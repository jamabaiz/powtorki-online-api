# Powtórki Online API

This repository contains the backend API for the "Powtórki Online" learning platform, built with FastAPI and SQLAlchemy.

### Page Types & Differences

The platform supports specialized page types to cater to different learning needs, implemented using SQLAlchemy's joined
table inheritance.

| Page Type      | ID | Description                   | Specific Features                                                              |
|:---------------|:---|:------------------------------|:-------------------------------------------------------------------------------|
| **Document**   | 2  | Standard educational content. |                                                                                |
| **Character**  | 4  | Biographical info.            |                                                                                |
| **Calendar**   | 5  | Historical dates/events.      | Linked to a `Date` model; Date as number (ordering) and text.                  |
| **Dictionary** | 6  | Terms and definitions.        |                                                                                |
| **QA**         | 7  | Simple Question & Answer.     |                                                                                |
| **Quiz**       | 8  | Interactive test.             | Supports multiple answers with correctness tracking and user activity logging. |

### Content Organization (Taxonomy)

Content is organized using a hierarchical taxonomy system defined in `app.database.models.taxonomy`.

- **Hierarchy Levels:**
    - **Subject (`SubjectTaxonomy`):** The top-level category (e.g., "History", "Civics").
    - **Chapter (`ChapterTaxonomy`):** Intermediate organization within a subject.
    - **Set (`SetTaxonomy`):** A specific collection of pages, usually the smallest unit of organization.
- **Navigation:** The system supports recursive navigation (ancestors and descendants) allowing for complex branching
  and content grouping.
- **Page Mapping:** Pages are linked to taxonomies via `MapPageTaxonomy`, which includes an `order_no` to maintain a
  specific sequence of materials within a chapter or set.

## Docs

Swagger at:
`/docs`

OpenApi at:
`/openapi.json`

## Installation

Create new env python 3.12+

`pip install -r requirements.txt`

## Run

To run development server from main directory type:

`uvicorn app.main:app --reload --header server:PowtorkiOnlineApi`

To run production server from main directory type:

`uvicorn app.main:app --workers 12 --header server:PowtorkiOnlineApi`