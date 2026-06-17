# Debugging Study Tickets

## Ticket #1: Investigation Required – test_create_update_user_status_wrong Failing

**Status:** FAILING TEST  
**Severity:** Medium  
**Description:**  
The test `test_create_update_user_status_wrong` in the test suite is failing with an assertion error. The test is making a PATCH request to update a user and checking the response status code. Investigate the failure, determine what the actual expected behavior should be, and correct the issue.

**Steps to Reproduce:**
- Run the test suite
- Observe the failure in `test_create_update_user_status_wrong`

**Expected Outcome:**  
Test should pass.


## Ticket #2: Silent Bug – Pagination Returns Wrong Records

**Status:** NEW TASK / INVESTIGATION  
**Severity:** High  
**Description:**  
QA reports that when fetching users with pagination, the paginated results don't align with expected record boundaries. For example, page 1 should return the first 10 users, and page 2 should return users 11-20, but the actual results appear offset. This has no failing test, but manual testing shows incorrect behavior.

**Steps to Reproduce:**
1. Create multiple users (15+)
2. Fetch `/api/users/?page=1&limit=10`
3. Fetch `/api/users/?page=2&limit=10`
4. Compare the actual records returned to expected boundaries

**Expected Outcome:**  
Page boundaries should align correctly; each page should return the correct set of records.  
**Action:**  
Manually reproduce the issue, write a test to capture the expected behavior, and fix the underlying cause.


## Ticket #3: User Creation Accepts Empty First Names

**Status:** NEW VALIDATION NEEDED  
**Severity:** Medium  
**Description:**  
The user creation endpoint currently accepts requests where the first_name field is an empty string. This should not be allowed. Requests with empty first names should be rejected with a validation error.

**Steps to Reproduce:**
1. Send a POST request to `/api/users/` with `first_name: ""`
2. Observe that the request may succeed instead of being rejected

**Expected Outcome:**  
Empty first names should be rejected with a 400 Bad Request error and a descriptive message.


## Ticket #4: User List Results Count Field Appears Inconsistent

**Status:** INVESTIGATION  
**Severity:** Low  
**Description:**  
The `results` field in the list users endpoint response may not accurately represent what a client would expect. Investigate what the `results` count is currently reporting (count of returned items vs. total matching items) and determine if the implementation matches the intended API contract. No specific test currently validates this behavior.

**Steps to Reproduce:**
1. Query the `/api/users/` endpoint with various limit and page combinations
2. Observe the `results` field in the response
3. Determine if it represents the count of items returned or total matching items

**Expected Outcome:**  
Clarify and document what the results field should represent, then ensure implementation matches intent.


## Ticket #5: Multi-Layer Issue – User Creation Payload Validation

**Status:** FAILING TEST / API CONTRACT  
**Severity:** High  
**Description:**  
There is a mismatch between the user creation schema and the underlying system regarding the `activated` field. Current API consumers may be unable to create users without explicitly specifying the activated status, even though the intended behavior might be to provide a sensible default. Investigate the schema definition, model defaults, and payload validation to identify where the disconnect occurs.

**Steps to Reproduce:**
- Attempt to create a user without providing an `activated` field
- Check what happens in the request/response flow

**Expected Outcome:**  
The activation status should have a consistent, well-defined default. Fix the issue at the appropriate layer (schema, model, or validation).


## Ticket #6: Regression Risk – User Update Endpoint Behavior Change

**Status:** TEST INVESTIGATION  
**Severity:** High  
**Description:**  
The user update (PATCH) endpoint may have a new constraint that prevents certain update scenarios that previously worked. Investigate the current update endpoint logic and determine if there are new restrictions on what fields can be modified or what values are now rejected. This may affect existing integrations.

**Steps to Reproduce:**
1. Try updating a user's address to a null/empty value
2. Observe whether it's accepted or rejected
3. Check if this is consistent with the original API design

**Expected Outcome:**  
Update endpoint should either support all valid field updates per the schema, or restrictions should be clearly intentional and well-justified.

---

**Suite is in expected state — work them in order.**
