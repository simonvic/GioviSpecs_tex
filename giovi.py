from pygments.lexer import RegexLexer, include, bygroups, using, this, inherit, default, words
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace


class GioviLexer(RegexLexer):
    name = 'Giovi'
    aliases = ['giovi']
    filenames = ['*.giovi']

    _character_escape = r'\\([btnfrs"\'\\${}]|u[a-fA-F0-9]{4})'

    tokens = {
        'root': [
            (r'[^\S\n]+', Whitespace),

            # unrolled version of r'(?s)#\{.*?\}#'
            # NOTE: it has to be matched before single line comments
            (r'#\{[^}]*\}+(?:[^#{][^{]*\}+)*#', Comment.Multiline),

            # Documentation line
            # (r'(#?.*?)(\n)', bygroups(Comment.Special, Whitespace)),

            (r'(#.*?)(\n)', bygroups(Comment.Single, Whitespace)),
            (r'"\{', String, 'normal_text_block'),
            (r'"', String, 'normal_text'),
            (r'\'\{', String, 'exact_text_block'),
            (r'\'', String, 'exact_text'),
            (
                words(
                    (
                        "if", "do", "else", "when", "for", "repeat", "break",
                        "skip", "return",
                        "default",
                        "self", "function", "tuple", "record", "struct",
                        "type",
                    ),
                    suffix=r'\b'
                ),
                Keyword
            ),
            (r'(var|const|alias)\b', Keyword.Declaration),
            (r'(not|and|or|in|is|as)\b', Operator.Word),
            (words(("true", "false", "_"), suffix=r'\b'), Keyword.Constant),
            (words(("import", "module"), suffix=r'\b'), Keyword.Namespace),
            (
                words(
                    ("Natural", "Int", "Real", "Text", "Void", "Bool",),
                    suffix=r'\b'
                ),
                Keyword.Type
            ),
            (words(("_out", "_err", "_in"), suffix=r'\b'), Name.Builtin),
            (r'=>', Keyword),
            (
                r'(::|<=|>=|<|>|~=|=~|!=|=|!|&|\||\+|-|\*|/|%|\^|@|\{>>\}|\{>\}|\{<\})',
                Operator
            ),
            (r'(\.|,|:|;|\[|\]|\{|\})', Punctuation),
            (r'([^\W\d]|\$)[\w$]*', Name),
            # kindly borrowed from java lexer :)
            (
                r'([0-9][0-9_]*\.([0-9][0-9_]*)?|'
                r'\.[0-9][0-9_]*)'
                r'(e[+\-]?[0-9][0-9_]*)?r?|'
                r'[0-9]e[+\-]?[0-9][0-9_]*r?|'
                r'[0-9](e[+\-]?[0-9][0-9_]*)?r|'
                r'0x([0-9a-fA-F][0-9a-fA-F_]*\.?|'
                r'([0-9a-fA-F][0-9a-fA-F_]*)?\.[0-9a-fA-F][0-9a-fA-F_]*)'
                r'p[+\-]?[0-9][0-9_]*r?',
                Number.Float
            ),
            (r'0x[0-9a-fA-F][0-9a-fA-F_]*[ni]?', Number.Hex),
            (r'0b[01][01_]*[ni]?', Number.Bin),
            (r'0o[0-7_]+[ni]?', Number.Oct),
            (r'0|[1-9][0-9_]*[ni]?', Number.Integer),
        ],
        'normal_text_block': [
            (r'[^\\\}]+', String),
            (_character_escape, String.Escape),
            (r'\}"', String, '#pop'),
            (r'\}', String),
        ],
        'normal_text': [
            (r'[^\\"\n]+', String),
            (_character_escape, String.Escape),
            (r'"', String, '#pop'),
        ],
        'exact_text_block': [
            (r'[^\\\}]+', String),
            (_character_escape, String.Escape),
            (r'\}\'', String, '#pop'),
            (r'\}', String),
        ],
        'exact_text': [
            (r'[^\\\'\n]+', String),
            (_character_escape, String.Escape),
            (r'\'', String, '#pop'),
        ],
    }
