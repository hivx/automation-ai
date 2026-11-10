Feature: <ID>
Stage: design
Author-agent: designer
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Design <ID> — <title>

## 1. Context
<excerpt from the spec; related architecture>

## 2. Data model
<entities, fields, constraints>

## 3. API / contract
<endpoint/function, inputs, outputs, errors; version>

## 4. Flow
1. <...>

## 5. Permissions
<who may do what; where it is checked>

## 6. Migration and rollback
- Up: <...>
- Down: <...>
- Reconciliation: <...>

## 7. Touchpoints
| file | change | notes |
|---|---|---|
| <path/to/file> | new / edit | <why it is touched; splitting into tasks is the tech-lead's job> |

## 8. Test plan
| Criterion | Test | Type |
|---|---|---|
| AC-1 | <test file::name> | unit / integration / e2e |
