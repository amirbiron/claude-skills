# Security Review Example
Input: Review this query construction for security risks.

```python
query = "SELECT * FROM users WHERE id = " + user_id
```

Expected direction: report a credible injection risk when user_id is untrusted, explain evidence and impact, and recommend parameterized queries.
