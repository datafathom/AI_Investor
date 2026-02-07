# Schema: Billing

## File Location
`schemas/billing.py`

## Purpose
Pydantic models for bill payment tracking, scheduling, reminders, and payment history. Supports the platform's bill pay functionality that helps users manage recurring expenses and avoid late payments.

---

## Enums

### BillStatus
**Current status of a bill.**

| Value | Description |
|-------|-------------|
| `PENDING` | Bill is awaiting payment |
| `SCHEDULED` | Payment has been scheduled |
| `PAID` | Bill has been paid |
| `OVERDUE` | Payment is past due date |
| `CANCELLED` | Bill was cancelled |

---

### RecurrenceType
**How often a bill recurs.**

| Value | Description |
|-------|-------------|
| `ONE_TIME` | Single payment, no recurrence |
| `WEEKLY` | Repeats every week |
| `MONTHLY` | Repeats monthly |
| `QUARTERLY` | Repeats every 3 months |
| `YEARLY` | Repeats annually |
| `CUSTOM` | User-defined recurrence schedule |

---

## Models

### Bill
**A bill to be tracked and paid.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `bill_id` | `str` | *required* | Unique bill identifier | Primary key, tracking |
| `user_id` | `str` | *required* | Owner of the bill | Access control |
| `bill_name` | `str` | *required* | User-friendly bill name | Display, search |
| `merchant` | `str` | *required* | Who the bill is paid to | Categorization, aggregation |
| `amount` | `float` | *required* | Bill amount in dollars | Payment processing |
| `due_date` | `datetime` | *required* | When payment is due | Reminder scheduling, overdue detection |
| `status` | `BillStatus` | `PENDING` | Current bill status | Workflow tracking |
| `recurrence` | `RecurrenceType` | `ONE_TIME` | How often bill repeats | Auto-scheduling future bills |
| `account_id` | `Optional[str]` | `None` | Payment account to use | Default payment source |
| `category` | `Optional[str]` | `None` | Expense category | Budgeting integration |
| `notes` | `Optional[str]` | `None` | User notes | Additional context |
| `created_date` | `datetime` | *required* | When bill was created | Audit trail |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### PaymentReminder
**Scheduled reminder for an upcoming or overdue bill.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `reminder_id` | `str` | *required* | Unique reminder identifier | Tracking, cancellation |
| `bill_id` | `str` | *required* | Associated bill | Links reminder to bill |
| `reminder_date` | `datetime` | *required* | When to send reminder | Scheduling |
| `reminder_type` | `str` | *required* | Type: `upcoming`, `due_soon`, `overdue` | Message content selection |
| `sent` | `bool` | `False` | Whether reminder was sent | Prevents duplicate sends |
| `sent_date` | `Optional[datetime]` | `None` | When reminder was sent | Audit trail |

---

### PaymentHistory
**Record of a completed payment.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `payment_id` | `str` | *required* | Unique payment identifier | Primary key |
| `bill_id` | `str` | *required* | Associated bill | Links payment to bill |
| `amount` | `float` | *required* | Amount paid | Financial tracking |
| `payment_date` | `datetime` | *required* | When payment was made | Timing |
| `payment_method` | `str` | *required* | How payment was made | Payment channel tracking |
| `confirmation_number` | `Optional[str]` | `None` | Payment confirmation ID | Verification, dispute resolution |
| `status` | `str` | *required* | Status: `completed`, `pending`, `failed` | Payment lifecycle |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `BillPaymentService` | CRUD operations, scheduling |
| `PaymentReminderService` | Notification scheduling and delivery |
| `BudgetingService` | Category-based spending analysis |
| `LinkedAccountService` | Payment account management |

## API Endpoints
- `POST /api/bills` - Create new bill
- `GET /api/bills` - List user's bills
- `PUT /api/bills/{id}` - Update bill
- `POST /api/bills/{id}/pay` - Initiate payment
- `GET /api/bills/reminders` - Get scheduled reminders

## Frontend Components
- Bill payment dashboard (FrontendBilling)
- Bill calendar view
- Payment history list
- Reminder configuration
