import json


def build_url_prompt(url: str, title: str, elements: dict) -> str:
    return f"""
  
You are a senior QA engineer.

- Distribute test coverage across the complete business journey
- Avoid over-concentrating on form validations or authentication flows
- Include realistic workflow variations and business scenarios
- Prioritize diverse business actions over repetitive field validations
Think like a real user and QA analyst before generating test cases.

First:
- Understand the business purpose
- Identify the primary user journey
- Identify critical workflows
- Identify possible failures and edge cases

Then generate realistic test coverage focusing on:
- End-to-end workflows
- Functional behavior
- User actions
- Accessibility
- Responsive behavior
- Negative scenarios
- Edge cases

Prioritize business-critical workflows over cosmetic UI checks.

Generate test cases based on business intent, not only visible UI elements.

Generate manual test cases in valid JSON format.


Return ONLY a JSON array.

IMPORTANT:
- All property names must use double quotes
- Do not use trailing commas
- Do not add explanations
- Do not add markdown
- Do not wrap JSON inside ```json
- Return valid parsable JSON only
- Do not generate plain text test cases

Each test case object must contain:

- "tc_id"
- "test_case_name"
- "action"
- "expected_result"
- "priority"
- "scenario_type"

Rules:
- "action" must be an array
- Each action step should be a separate string
- Generate concise professional QA test cases
- Generate balanced Functional, Negative, Edge, Accessibility, and Responsive coverage
- Focus on realistic business workflows and user journeys
- Avoid excessive form validation scenarios unless business critical
- Do not generate security scenarios
- Exclude SQL injection and XSS cases
- Avoid duplicate test cases
- Prioritize the user requested workflow over currently visible UI elements
- Prioritize the primary business functionality of the application
- Focus more on the main user journey than authentication pages
- Generate authentication test cases only when login is a required prerequisite
- For booking, ecommerce, travel, or ordering websites:
  prioritize search,
  selection,
  cart,
  checkout,
  payment,
  and confirmation workflows
- If the prompt mentions end-to-end flow, generate test cases for the complete business flow
- Do not limit test generation to the landing page only
- Include downstream workflow scenarios when explicitly mentioned in user requirements

Example format:

[
  {{
    "tc_id": "TC001",
    "test_case_name": "Verify successful login",
    "action": [
      "Open login page",
      "Enter valid username",
      "Enter valid password",
      "Click Login button"
    ],
    "expected_result": "User logs in successfully",
    "priority": "High",
    "scenario_type": "Functional"
  }}
]
USER WORKFLOW REQUIREMENT:
Generate test cases based on the user's requested flow and business journey, not only the currently loaded page.
Page URL:
{url}

Page Title:
{title}


CRAWLED APPLICATION FLOW:

The following pages were crawled sequentially as part of the user journey.

Generate test cases covering:
- end-to-end workflows
- cross-page validations
- business workflows
- realistic navigation paths
- booking and checkout journeys

Crawled Pages:
{json.dumps(elements, indent=2)}
""".strip()


def build_ac_prompt(ac_text: str) -> str:
    return f"""
You are a senior QA engineer...  

- Distribute test coverage across the complete business journey
- Avoid over-concentrating on form validations or authentication flows
- Include realistic workflow variations and business scenarios
- Prioritize diverse business actions over repetitive field validations
Generate manual test cases in valid JSON format.



Think like a real user and QA analyst before generating test cases.

First:
- Understand the business purpose
- Identify the primary user journey
- Identify critical workflows
- Identify possible failures and edge cases

Then generate realistic test coverage focusing on:
- End-to-end workflows
- Functional behavior
- User actions
- Accessibility
- Responsive behavior
- Negative scenarios
- Edge cases

Prioritize business-critical workflows over cosmetic UI checks.

Generate test cases based on business intent, not only visible UI elements.

Generate manual test cases in valid JSON format.

Return ONLY a JSON array.

IMPORTANT:
- All property names must use double quotes
- Do not use trailing commas
- Do not add explanations
- Do not add markdown
- Do not wrap JSON inside ```json
- Return valid parsable JSON only
- Do not generate plain text test cases

Each test case object must contain:

- "tc_id"
- "test_case_name"
- "action"
- "expected_result"
- "priority"
- "scenario_type"

Generate comprehensive professional QA test cases.

IMPORTANT COVERAGE REQUIREMENTS:

Generate only these scenario types:
- Functional
- Negative
- Edge
- Accessibility
- Responsive
IMPORTANT:
- Do not generate scenario types outside this list
- Do not use:
  Positive,
  Validation,
  Security,
  Regression,
  Navigation,
  Usability,
  UI Testing,
  Edge Case
- Use exact scenario type values only

Do not generate:
- Security test cases
- SQL Injection scenarios
- XSS scenarios
- Authentication attack scenarios
- Penetration testing scenarios

Coverage Expectations:

- Include strong functional coverage
- Include UI validation scenarios
- Include negative and edge cases
- Include accessibility scenarios
- Include error handling scenarios

- Generate realistic QA scenarios, not generic UI observations
- Focus on user behavior and business workflows
- Avoid repetitive test cases like:
  "View button"
  "Observe layout"
  "Check alignment"
- Include meaningful validations and interactions
- Include keyboard and screen reader coverage where relevant
- Include responsive validations for mobile breakpoints
- Include realistic failure and recovery scenarios
- Do not invent backend, API, or loading behaviors unless implied in requirements
- Avoid low value edge cases like double click validations unless explicitly required
- Prefer meaningful edge cases involving:
  state handling,
  responsiveness,
  empty data,
  long content,
  rapid interactions,
  loading failures,
  and accessibility behavior
- Prioritize functional behavior over cosmetic checks
- Do not invent unsupported features or gestures
- Do not assume unsupported keyboard shortcuts or interactions
- Use only standard accessibility interactions unless explicitly specified
- Avoid generating swipe, pinch, drag, or voice interactions unless explicitly mentioned
- Avoid unrealistic browser or device behavior validations

IMPORTANT:
- Keep every test case concise
- Action steps should represent realistic user workflows
- Avoid generic actions without validation intent
- Every test case should validate behavior, state, or usability
- Maximum 3 action steps per test case
- Keep expected_result short
- Use concise professional QA wording
- Prefer:
  displayed,
  hidden,
  visible,
  announced,
  accessible,
  triggered,
  updated
- Avoid robotic phrases like:
  "effect is triggered",
  "works properly",
  "functions correctly"
- Expected results should validate system behavior clearly
- Scenario types must match the actual validation intent
- Do not classify responsive or UI validations as Negative scenarios
- Avoid vague terms like:
  visually,
  properly,
  correctly
- Prefer measurable validation outcomes
- Keep test_case_name short
- Do not generate lengthy descriptions
- Generate the appropriate number of test cases based on requirement complexity
- Prioritize meaningful coverage over quantity
- Avoid artificially increasing test case count
- Number of test cases can vary based on application complexity
- Focus on quality over quantity
- Avoid repetitive scenarios
- Every test case must include a meaningful user interaction or validation
- Avoid passive test cases like:
  "View button"
  "Observe layout"
  "Check alignment"
  "Verify screen"
- Prefer action-driven scenarios:
  click,
  navigate,
  resize,
  expand,
  collapse,
  submit,
  retry,
  toggle,
  validate
- Cover all meaningful workflows and validations
- Action steps must describe real user interaction
- Prefer action + validation flows
- Avoid vague actions like:
  "View button"
  "Observe screen"
- Use maximum 2 action steps where possible
- Keep expected_result under 12 words
- Avoid repeating full URLs in every test case
- Use concise navigation steps
- Prioritize the most important and realistic user workflows.
- Avoid duplicate scenarios
- Cover all identified pages and workflows
- Keep action steps concise
- Reuse workflow context intelligently across related test cases
- Do not restart every test case from homepage or login page
- Avoid repeatedly using:
  "Navigate to homepage",
  "Open website",
  "Launch application",
  "Login if required"
unless necessary for the scenario

- Combine obvious sequential UI interactions into concise business actions
- Prefer:
  "Search journey with valid stations"
instead of:
  "Enter departure station",
  "Enter arrival station",
  "Select date",
  "Click search"

- Prefer business-oriented actions over low-level UI interactions
- Avoid expanding every click and input into separate steps unless necessary

- Assume the user is already on the relevant workflow page when appropriate
- Focus action steps on the actual validation being tested
- Keep setup steps minimal and non repetitive
- Avoid unnecessary navigation actions when the workflow context is already implied
- Use concise business-oriented action steps

Example format:

[
  {{
    "tc_id": "TC001",
    "test_case_name": "Verify successful login",
    "action": [
      "Open login page",
      "Enter valid username",
      "Enter valid password",
      "Click Login button"
    ],
    "expected_result": "User logs in successfully",
    "priority": "High",
    "scenario_type": "Functional"
  }}
]

Acceptance Criteria:
{ac_text}
""".strip()
