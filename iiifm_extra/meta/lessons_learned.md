## BOP Popup Questions Discovery Pattern

**Lesson**: BOP popup questions use hybrid loading - don't rely only on static ASCX markup. Check for dynamic kill questions loaded via `UWQuestions.GetKillQuestions()` method + hardcoded conditional questions. Total found: 6 dynamic + 5 static = 11 questions.

**Key**: Always verify both loading patterns exist before concluding question count. Static markup analysis alone will miss dynamically loaded questions.

---

## WCP QuickQuote Popup Questions Discovery Pattern

**Lesson**: WCP popup questions are entirely QuickQuote system-driven. Found 6 kill questions in `UWQuestions.GetCommercialWCPUnderwritingQuestions()` method via `QuickQuoteObject.QuickQuoteLobType.WorkersCompensation` case handling.

**Key**: VelociRater IS built on QuickQuote framework - the UWQuestions system IS the "quick quote object" method. Diamond codes 9341, 9086, 9342/9573, 9343, 9344, 9107 confirmed as WCP kill questions.

---