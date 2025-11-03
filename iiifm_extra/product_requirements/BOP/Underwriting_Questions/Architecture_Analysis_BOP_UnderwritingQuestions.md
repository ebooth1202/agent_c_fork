# Architecture Analysis: BOP Underwriting Questions Modernization

**Line of Business**: Business Owner's Policy (BOP)  
**Feature**: Underwriting Questions  
**Document Type**: Architecture Analysis  
**Analyst**: Aria (IFI Architecture Specialist)  
**Date**: 2024-12-19  
**Status**: Complete

---

## Executive Summary

Architecture analysis reveals a sophisticated dual-system questionnaire platform built on legacy ASP.NET WebForms with embedded domain logic and complex UI state management. The current implementation successfully manages 11 primary questions (6 kill questions + 5 standard questions) through a rich domain model (VRUWQuestion) with extensive business rules. Key modernization opportunities include domain-driven design extraction, event-driven architectures, and modern UI framework migration while preserving regulatory compliance and business logic integrity.

**Architecture Quality Assessment**: Current system demonstrates solid domain modeling with the VRUWQuestion class but suffers from typical WebForms architectural limitations including tight UI coupling, mixed concerns, and monolithic control structures.

---

## Current Architecture Analysis

### 1. Domain Architecture Pattern

#### VRUWQuestion Domain Entity Analysis
**Source Evidence**: `UWQuestions.vb:9690-9779`

```vb
Public Class VRUWQuestion
    Inherits QuickQuotePolicyUnderwriting
    Implements ICloneable
    
    Public Property QuestionNumber As Int32
    Public Property Description As String
    Public Property kqDescription As String
    Public Property IsTrueKillQuestion As Boolean
    Public Property IsTrueUwQuestion As Boolean
    Public Property SectionName As String
    Public Property IsQuestionRequired As Boolean
    Public Property NeverShowDescription As Boolean
    Public Property AlwaysShowDescription As Boolean
    ' ... 20+ additional properties
End Class
```

**Architectural Assessment**:
- ✅ **Rich Domain Object**: 30+ properties encapsulating question behavior and state
- ✅ **Business Logic Integration**: Calculated properties (Answer, HasBeenAnswered)
- ⚠️ **Persistence Coupling**: Inherits from QuickQuotePolicyUnderwriting (data layer coupling)
- ⚠️ **Mixed Concerns**: UI display properties mixed with domain logic

#### Question Classification System
**Source Evidence**: `UWQuestions.vb:1067-1199`

```vb
' Kill Questions (Required)
list.Add(New VRUWQuestion() With {
    .Description = "3. Any exposure to flammables, explosives, chemicals?",
    .PolicyUnderwritingCodeId = "9003",
    .IsQuestionRequired = True,
    .kqDescription = "Any exposure to flammables, explosives, chemicals?"
})

' Standard Questions (Optional)  
list.Add(New VRUWQuestion() With {
    .Description = "1A. Is the Applicant a subsidiary of another entity?",
    .PolicyUnderwritingCodeId = "9000",
    .IsQuestionRequired = False
})
```

**Architectural Pattern Analysis**:
- **Kill Questions**: Codes {9003, 9006, 9007, 9008, 9009, 9400} with business impact
- **True Kill Question**: Code 9008 (IsTrueKillQuestion = True) immediately archives quote
- **Standard Questions**: Information collection without binding impact
- **Section Grouping**: Unified "Applicant Information" section for all 11 questions

### 2. Dual System Architecture Pattern

#### Kill Question Filtering Logic
**Source Evidence**: `UWQuestions.vb:54-55`

```vb
Dim killQuestionCodes As New List(Of String) From {"9003", "9006", "9007", "9008", "9009", "9400"}
Dim kq As List(Of VRUWQuestion) = (From uw In GetCommercialBOPUnderwritingQuestions() 
                                   Where killQuestionCodes.Contains(uw.PolicyUnderwritingCodeId) 
                                   Select uw).ToList()
```

**Architectural Pattern**:
- **Single Source of Truth**: Complete question set defined once
- **Dynamic Filtering**: Kill questions extracted via LINQ query
- **Context-Sensitive Display**: Same questions appear in popup vs. application contexts
- **Sequential Numbering**: Dynamic numbering (1-6) applied to kill questions in popup

#### Dual Control Implementation
**Source Evidence**: 
- Popup: `ctlUWQuestionsPopup.ascx` (modal dialog)
- Application: `ctlCommercialUWQuestionItem.ascx` (form section)

**Architecture Benefits**:
- ✅ **Code Reuse**: Single question definition shared across contexts
- ✅ **Data Consistency**: Same business logic applied in both contexts
- ⚠️ **Maintenance Complexity**: Two UI implementations requiring synchronization

### 3. UI Architecture Patterns

#### WebForms Control Architecture
**Source Evidence**: `ctlCommercialUWQuestionItem.ascx`

```asp
<asp:Repeater ID="rptUWQ" runat="server">
    <ItemTemplate>
        <table class='<%# "questionTable " + DataBinder.Eval(Container.DataItem, "PolicyUnderwritingCodeId") %>'>
            <tr>
                <td><asp:Label Text='<%# DataBinder.Eval(Container.DataItem, "Description")%>' /></td>
                <td>
                    <asp:RadioButton ID="rbNo" Text="No" GroupName="Group0" />
                    <asp:RadioButton ID="rbYes" Text="Yes" GroupName="Group0" />
                </td>
            </tr>
        </table>
        <table class='<%# "DescriptionTable " + IIf(DataBinder.Eval(Container.DataItem, "AlwaysShowDescription") = True, "alwaysShow", "") %>'>
            <tr>
                <td>
                    <asp:TextBox ID="txtUWQDescription" TextMode="MultiLine" maxLength="125" 
                                OnKeyUp="CheckMaxTextNoDisable(this, 125);" />
                </td>
            </tr>
        </table>
    </ItemTemplate>
</asp:Repeater>
```

**UI Architecture Assessment**:
- ✅ **Data Binding**: Clean separation of data and presentation
- ✅ **Dynamic CSS Classes**: Conditional styling based on question properties
- ⚠️ **Table-Based Layout**: Legacy HTML structure limits responsive design
- ⚠️ **Server Control Overhead**: Heavy ViewState and postback model

#### Dynamic Panel Management
**Source Evidence**: `ctlUWQuestionsPopup.ascx` JavaScript functions

```javascript
function ShowHideAdditionalInfo() {
    $('#tblKillQuestions > tbody  > tr, .tblBOPKillQuestions > tbody  > tr').each(function () {
        if (index % 2 == 0) {
            if ($(this).find('input').first().is(':checked')) {
                $(this).next().show();
            }
            else {
                $(this).next().hide();
            }
        }
        index += 1;
    });
}
```

**Client-Side Architecture Patterns**:
- **Event-Driven UI**: Radio button changes trigger panel visibility
- **jQuery DOM Manipulation**: Direct DOM traversal and modification
- **Conditional Display Logic**: Business rules embedded in JavaScript

### 4. Validation Architecture

#### Character Limit Validation (BOP-Specific)
**Source Evidence**: `ctlCommercialUWQuestionItem.ascx:36`

```asp
<asp:TextBox maxLength="125" OnKeyUp="CheckMaxTextNoDisable(this, 125);" 
             OnPaste="CheckMaxTextNoDisable(this, 125);" />
```

**Validation Pattern Analysis**:
- **Real-Time Validation**: Character counting on keystroke and paste
- **LOB-Specific Limits**: 125 characters specifically for BOP (different from other LOBs)
- **Visual Feedback**: Red borders, error messages, character counters
- **NoDisable Variant**: BOP uses special validation that doesn't disable submit button

#### Form Validation Logic
**Source Evidence**: `ctlUWQuestionsPopup.ascx` ValidateUWForm() function

```javascript
function ValidateUWForm() {
    var a1 = AllAnswersAreAnswered()
    var a2 = AllAdditionalInfoFieldsAreAnswered();
    var a5 = AllBOPAdditionalInfoFieldsAreAnswered();
    return (a1 && a2 && a5 && /* other validations */);
}
```

**Validation Architecture**:
- **Composite Validation**: Multiple validation functions combined
- **LOB-Specific Functions**: Separate validation for each line of business
- **User Experience**: Visual indicators before submission blocked

### 5. Data Persistence Architecture

#### Answer Value Mapping
**Source Evidence**: `ctlCommercialUWQuestionItem.ascx.vb:76-82`

```vb
qqItem.PolicyUnderwritingAnswer = If(radioYes.Checked, "1", If(radioNo.Checked, "-1", "0"))
qqItem.PolicyUnderwritingCodeId = question(0).PolicyUnderwritingCodeId
qqItem.PolicyUnderwritingExtraAnswer = txtAdditionInfo.Text
```

**Persistence Pattern Analysis**:
- **Value Mapping**: Yes=1, No=-1, Unanswered=0
- **Diamond Code Integration**: Regulatory compliance through code mapping
- **Additional Information**: Text content with 125-character database limit
- **Multi-State Support**: SubQuotes collection for state-specific persistence

#### Save Operation Flow
**Source Evidence**: `ctlCommercialUWQuestionItem.ascx.vb:45-180`

1. **Question Loading**: GetCommercialBOPUnderwritingQuestions()
2. **Form Processing**: Iterate through Repeater items
3. **Data Mapping**: Convert UI controls to domain objects  
4. **Multi-State Persistence**: Add to SubQuotes collection
5. **Database Storage**: QuickQuotePolicyUnderwriting entities

---

## Domain-Driven Design Analysis

### Bounded Context Identification

#### BOP Underwriting Questions Context
**Domain Boundaries**:
- **Question Management**: Question definition, classification, and configuration
- **Answer Processing**: Response capture, validation, and persistence
- **Business Rules**: Kill question logic, conditional requirements, additional information rules

#### Integration Points
- **Diamond Regulatory System**: Question code compliance and audit trails
- **VelociRater Quote Engine**: Question responses impact rating and binding
- **UI Framework**: Question presentation and user interaction management

### Aggregate Design Recommendations

#### QuestionnaireAggregate
```csharp
public class QuestionnaireAggregate : AggregateRoot<QuestionnaireId>
{
    private List<UWQuestion> _questions;
    private List<QuestionResponse> _responses;
    
    public void AnswerQuestion(QuestionId questionId, Answer answer, string additionalInfo);
    public void ValidateCompleteness();
    public bool IsKillQuestionAnsweredYes();
    public void ProcessTrueKillQuestion();
}
```

#### UWQuestion Entity
```csharp
public class UWQuestion : Entity<QuestionId>
{
    public QuestionType Type { get; private set; } // Kill, Standard, TrueKill
    public DiamondCode RegulatorCode { get; private set; }
    public string Description { get; private set; }
    public bool IsRequired { get; private set; }
    public AdditionalInfoPolicy InfoPolicy { get; private set; }
}
```

#### QuestionResponse ValueObject  
```csharp
public class QuestionResponse : ValueObject
{
    public Answer Answer { get; private set; } // Yes, No, Unanswered
    public AdditionalInfo AdditionalInformation { get; private set; }
    public DateTime AnsweredAt { get; private set; }
    
    protected override IEnumerable<object> GetAtomicValues()
    {
        yield return Answer;
        yield return AdditionalInformation?.Value;
        yield return AnsweredAt;
    }
}
```

---

## Modernization Architecture Recommendations

### 1. Event-Driven Architecture Implementation

#### Domain Events
```csharp
public class QuestionAnsweredEvent : DomainEvent
{
    public QuestionId QuestionId { get; }
    public Answer Answer { get; }
    public bool IsKillQuestion { get; }
    public string AdditionalInfo { get; }
}

public class TrueKillQuestionTriggeredEvent : DomainEvent
{
    public QuestionnaireId QuestionnaireId { get; }
    public QuoteId QuoteId { get; }
    public string Reason { get; }
}
```

#### Event Handlers
```csharp
public class QuestionAnsweredEventHandler : IEventHandler<QuestionAnsweredEvent>
{
    public async Task Handle(QuestionAnsweredEvent @event)
    {
        // Trigger additional information panel display
        // Update validation state
        // Log answer for audit trail
    }
}

public class TrueKillQuestionEventHandler : IEventHandler<TrueKillQuestionTriggeredEvent>
{
    public async Task Handle(TrueKillQuestionTriggeredEvent @event)
    {
        // Archive quote immediately
        // Navigate user to MyVelocirater
        // Notify underwriting system
    }
}
```

### 2. CQRS Pattern Implementation

#### Command Side
```csharp
public class AnswerQuestionCommand : ICommand
{
    public QuestionnaireId QuestionnaireId { get; set; }
    public QuestionId QuestionId { get; set; }
    public Answer Answer { get; set; }
    public string AdditionalInformation { get; set; }
}

public class AnswerQuestionCommandHandler : ICommandHandler<AnswerQuestionCommand>
{
    public async Task<Result> Handle(AnswerQuestionCommand command)
    {
        var questionnaire = await _repository.GetByIdAsync(command.QuestionnaireId);
        questionnaire.AnswerQuestion(command.QuestionId, command.Answer, command.AdditionalInformation);
        await _repository.SaveAsync(questionnaire);
        return Result.Success();
    }
}
```

#### Query Side
```csharp
public class GetBOPUnderwritingQuestionsQuery : IQuery<List<UWQuestionDto>>
{
    public LOBType LOB { get; set; } = LOBType.BOP;
    public QuestionContext Context { get; set; } // Popup vs Application
}

public class UWQuestionDto
{
    public string QuestionId { get; set; }
    public string Description { get; set; }
    public string DiamondCode { get; set; }
    public bool IsRequired { get; set; }
    public bool IsKillQuestion { get; set; }
    public bool IsTrueKillQuestion { get; set; }
    public AdditionalInfoPolicy InfoPolicy { get; set; }
    public Answer? CurrentAnswer { get; set; }
    public string AdditionalInfo { get; set; }
}
```

### 3. Modern API Design

#### RESTful Question Management API
```csharp
[ApiController]
[Route("api/underwriting/questionnaires")]
public class QuestionnaireController : ControllerBase
{
    [HttpGet("{lobType}/questions")]
    public async Task<ActionResult<List<UWQuestionDto>>> GetQuestions(
        LOBType lobType, 
        [FromQuery] QuestionContext context = QuestionContext.Application)
    {
        var query = new GetBOPUnderwritingQuestionsQuery 
        { 
            LOB = lobType, 
            Context = context 
        };
        return await _mediator.Send(query);
    }

    [HttpPost("{questionnaireId}/answers")]
    public async Task<ActionResult> AnswerQuestion(
        Guid questionnaireId,
        [FromBody] AnswerQuestionCommand command)
    {
        command.QuestionnaireId = new QuestionnaireId(questionnaireId);
        var result = await _mediator.Send(command);
        return result.IsSuccess ? Ok() : BadRequest(result.Error);
    }

    [HttpGet("{questionnaireId}/validation")]
    public async Task<ActionResult<ValidationResultDto>> ValidateCompleteness(Guid questionnaireId)
    {
        var query = new ValidateQuestionnaireQuery { QuestionnaireId = new QuestionnaireId(questionnaireId) };
        return await _mediator.Send(query);
    }
}
```

### 4. Modern UI Architecture

#### React Component Structure
```typescript
// Question Management Container
export const UnderwritingQuestionnaire: React.FC<QuestionnaireProps> = ({ 
    lobType, 
    context, 
    onComplete 
}) => {
    const { questions, loading } = useQuestions(lobType, context);
    const { answers, updateAnswer } = useAnswers();
    const { validation, validate } = useValidation();

    return (
        <div className="questionnaire-container">
            {questions.map(question => (
                <UnderwritingQuestion
                    key={question.questionId}
                    question={question}
                    answer={answers[question.questionId]}
                    onAnswerChange={updateAnswer}
                />
            ))}
            <ValidationSummary validation={validation} />
            <QuestionnaireActions onSubmit={handleSubmit} />
        </div>
    );
};

// Individual Question Component
export const UnderwritingQuestion: React.FC<QuestionProps> = ({
    question,
    answer,
    onAnswerChange
}) => {
    const showAdditionalInfo = answer?.answer === Answer.Yes || question.alwaysShowAdditionalInfo;

    return (
        <div className={`question ${question.isRequired ? 'required' : ''}`}>
            <QuestionText text={question.description} required={question.isRequired} />
            <AnswerRadioGroup
                value={answer?.answer}
                onChange={(ans) => onAnswerChange(question.questionId, ans, answer?.additionalInfo)}
            />
            {showAdditionalInfo && (
                <AdditionalInfoPanel
                    value={answer?.additionalInfo}
                    maxLength={125}
                    onChange={(info) => onAnswerChange(question.questionId, answer?.answer, info)}
                />
            )}
        </div>
    );
};
```

#### State Management (Redux Toolkit)
```typescript
// Question Slice
export const questionSlice = createSlice({
    name: 'questions',
    initialState: {
        questions: [],
        answers: {},
        validation: { isValid: false, errors: [] },
        loading: false
    },
    reducers: {
        answerQuestion: (state, action) => {
            const { questionId, answer, additionalInfo } = action.payload;
            state.answers[questionId] = { answer, additionalInfo, answeredAt: new Date() };
            
            // Trigger validation
            state.validation = validateQuestionnaire(state.questions, state.answers);
            
            // Handle kill question logic
            if (isKillQuestion(state.questions, questionId) && answer === Answer.Yes) {
                // Dispatch additional events for kill question handling
            }
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchQuestions.fulfilled, (state, action) => {
                state.questions = action.payload;
            })
            .addCase(submitAnswers.fulfilled, (state, action) => {
                // Handle successful submission
            });
    }
});
```

### 5. Integration Modernization

#### Diamond System Integration
```csharp
public class DiamondComplianceService : IDiamondComplianceService
{
    public async Task<ComplianceResult> ValidateQuestionCompliance(
        List<QuestionResponse> responses, 
        string state)
    {
        var diamondCodes = responses.Select(r => r.Question.DiamondCode);
        return await _diamondApiClient.ValidateUnderwritingQuestions(diamondCodes, state);
    }

    public async Task<AuditTrail> CreateAuditTrail(QuestionnaireId questionnaireId)
    {
        // Create regulatory audit trail for Diamond system
        var questionnaire = await _repository.GetByIdAsync(questionnaireId);
        return new AuditTrail
        {
            QuestionnaireId = questionnaireId,
            Responses = questionnaire.Responses.Select(r => new AuditEntry
            {
                DiamondCode = r.Question.DiamondCode,
                Answer = r.Answer.ToString(),
                AdditionalInfo = r.AdditionalInformation?.Value,
                Timestamp = r.AnsweredAt
            }).ToList()
        };
    }
}
```

#### VelociRater Integration
```csharp
public class QuoteImpactService : IQuoteImpactService
{
    public async Task<QuoteImpact> AnalyzeQuestionnaireImpact(
        QuestionnaireId questionnaireId, 
        QuoteId quoteId)
    {
        var questionnaire = await _repository.GetByIdAsync(questionnaireId);
        
        // Check for true kill question
        if (questionnaire.HasTrueKillQuestionAnsweredYes())
        {
            return new QuoteImpact
            {
                Action = QuoteAction.Archive,
                Reason = "True kill question answered yes",
                NavigationTarget = "MyVelocirater"
            };
        }

        // Analyze other kill questions
        var killQuestions = questionnaire.GetKillQuestionsAnsweredYes();
        return new QuoteImpact
        {
            Action = killQuestions.Any() ? QuoteAction.RequireUnderwritingReview : QuoteAction.Continue,
            AdditionalInformationRequired = killQuestions.Any(),
            UnderwritingFlags = killQuestions.Select(q => q.DiamondCode).ToList()
        };
    }
}
```

---

## Migration Strategy

### Phase 1: Domain Model Extraction (2-3 months)
1. **Extract Domain Logic**: Create QuestionnaireAggregate, UWQuestion, QuestionResponse
2. **Implement Repository Pattern**: Abstract data access from current WebForms controls
3. **Add Unit Testing**: Test domain logic independently of UI framework
4. **Preserve Current UI**: Keep existing WebForms while building domain layer

### Phase 2: API Development (2-3 months)
1. **Build CQRS Infrastructure**: Command/Query handlers with MediatR
2. **Implement REST APIs**: Question retrieval, answer submission, validation endpoints
3. **Add Integration Layer**: Diamond compliance service, VelociRater impact service
4. **API Testing**: Comprehensive integration testing for backward compatibility

### Phase 3: Modern UI Implementation (3-4 months)
1. **React Component Development**: Build questionnaire components with TypeScript
2. **State Management**: Redux Toolkit for client-side state management
3. **Real-Time Validation**: Implement character limits, required field validation
4. **Responsive Design**: Mobile-friendly question presentation
5. **Accessibility Compliance**: WCAG 2.1 AA compliance for screen readers

### Phase 4: Event-Driven Enhancements (1-2 months)
1. **Domain Events**: Implement question answered, kill question triggered events
2. **Event Handlers**: Business logic for kill question processing, audit trail creation
3. **Notification System**: Real-time UI updates based on domain events
4. **Performance Optimization**: Caching strategies for question metadata

### Phase 5: Legacy Migration (2-3 months)
1. **Gradual Cutover**: Feature flag controlled migration per LOB
2. **Data Migration**: Migrate existing question responses to new domain model
3. **Monitoring & Rollback**: Comprehensive monitoring with rollback capability
4. **Training & Documentation**: User guides for new question interface

---

## Risk Assessment & Mitigation

### Technical Risks

#### Risk: Regulatory Compliance Disruption
**Likelihood**: Medium | **Impact**: High
**Mitigation Strategy**:
- Maintain Diamond code mapping integrity throughout migration
- Implement comprehensive audit trail preservation
- Parallel run testing with regulatory validation
- Regulatory approval for architectural changes

#### Risk: Kill Question Logic Failure  
**Likelihood**: Low | **Impact**: High
**Mitigation Strategy**:
- Extensive unit testing for kill question business logic
- Integration testing for true kill question processing (9008)
- Canary deployment for kill question validation
- Rollback capability for kill question failures

#### Risk: Performance Degradation
**Likelihood**: Medium | **Impact**: Medium
**Mitigation Strategy**:
- Load testing for question loading and validation
- Caching strategies for question metadata
- API response time monitoring
- Progressive loading for large question sets

### Business Risks

#### Risk: User Experience Disruption
**Likelihood**: Medium | **Impact**: Medium  
**Mitigation Strategy**:
- Phased rollout with user feedback collection
- A/B testing for UI improvements
- Training materials for agents and underwriters
- Support channel enhancement during migration

#### Risk: Integration Failures
**Likelihood**: Medium | **Impact**: High
**Mitigation Strategy**:
- Comprehensive integration testing with Diamond and VelociRater
- Mock services for testing isolation
- Circuit breaker patterns for external dependencies
- Fallback mechanisms for integration failures

---

## Success Metrics

### Technical Metrics
- **Question Loading Performance**: < 2 seconds for all 11 BOP questions
- **Real-Time Validation Response**: < 100ms for character limit validation
- **Form Submission Processing**: < 3 seconds for complete questionnaire
- **API Response Times**: < 500ms for question retrieval, < 1 second for answer submission
- **Error Rate**: < 0.1% for question processing operations

### Business Metrics
- **Question Completion Rate**: ≥ 95% completion rate for required kill questions
- **User Satisfaction**: ≥ 4.0/5.0 rating for new question interface
- **Underwriter Efficiency**: 20% reduction in question review time
- **Regulatory Compliance**: 100% audit trail accuracy for regulatory examination
- **System Reliability**: 99.9% uptime for question processing

### Code Quality Metrics
- **Unit Test Coverage**: ≥ 90% for domain logic, ≥ 80% for application services
- **Integration Test Coverage**: 100% for kill question scenarios
- **Code Maintainability**: Maintainability Index > 75
- **Technical Debt Reduction**: 50% reduction in cyclomatic complexity

---

## Conclusion

The BOP Underwriting Questions system demonstrates solid domain modeling foundations with the VRUWQuestion class but requires modernization to improve maintainability, user experience, and development velocity. The recommended domain-driven design approach preserves business logic while enabling modern architectural patterns including CQRS, event-driven processing, and API-first design.

**Key Success Factors**:
1. **Regulatory Compliance Preservation**: Maintain Diamond code integration and audit trail capabilities
2. **Kill Question Logic Integrity**: Preserve complex business rules for kill question processing
3. **Phased Migration Approach**: Minimize risk through gradual modernization with rollback capability
4. **Domain Expertise Retention**: Involve current system experts throughout modernization process

**Recommended Next Steps**:
1. **Rita Insurance Domain Validation**: Review architectural recommendations for regulatory compliance impact
2. **Technical Proof of Concept**: Build domain model extraction prototype for kill question logic
3. **Stakeholder Alignment**: Confirm modernization priorities with business stakeholders
4. **Resource Planning**: Allocate development team for 10-12 month modernization timeline

The proposed architecture provides a foundation for scalable, maintainable underwriting question management while preserving the business value and regulatory compliance of the current system.

---

## Appendix: Source Code References

### Primary Source Files Analyzed
- `UWQuestions.vb` (lines 1012-1447): BOP question definitions and domain logic
- `ctlCommercialUWQuestionItem.ascx`: BOP-specific UI control implementation  
- `ctlCommercialUWQuestionItem.ascx.vb`: Question processing and persistence logic
- `ctlUWQuestionsPopup.ascx`: Kill question popup modal implementation
- `VRUWQuestion` class (lines 9690-9779): Domain entity structure and behavior

### Key Methods and Functions
- `GetCommercialBOPUnderwritingQuestions()`: Primary question loading (line 1012)
- `GetKillQuestions()`: Kill question filtering logic (lines 54-55)
- `Save()`: Question response persistence (ctlCommercialUWQuestionItem.ascx.vb:45)
- `ValidateUWForm()`: Client-side validation orchestration (ctlUWQuestionsPopup.ascx)

**Document Prepared By**: Aria (IFI Architecture Specialist)  
**Evidence-Based Analysis**: All architectural patterns verified with source code references  
**Ready for**: Rita (Insurance Domain Validation) - Juncture 4 Critical Handoff