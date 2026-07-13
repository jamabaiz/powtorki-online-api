class KnowledgeTypes:
    History = 1
    Civics = 2


class PageTypes:
    """
    Defines page handling logic
    """
    Page = 1
    DocumentPage = 2
    CharacterPage = 4
    CalendarPage = 5
    DictionaryPage = 6
    QAPage = 7
    QuizPage = 8


class PageSubTypes:
    """
    Defines variants of page types (same logic different scope)
    """
    VideoScriptPage = 1
    # ProofPage = 2
    # ExperimentPage = 3
    MindmapPage = 4
    ScriptPage = 5
    DocumentPage = 6
    Character = 7
    Date = 8
    Dictionary = 9
    QA = 10
    Quiz = 11
    # TheoremPage = 12


class TaxonomyTypes:
    """
    Defines taxonomy logic scope
    """
    Taxonomy = 1
    SubjectTaxonomy = 2
    ChapterTaxonomy = 3
    SetTaxonomy = 4


class Roles:
    Admin = 'admin'
    User = 'user'
    map_id_to_name = {
        1: "admin",
        2: 'user',
    }


class ActivitySettings:
    correct_answer = 1
    incorrect_answer = -2
    page_read = 0.25
