import re

import sqlparse

SQL = """-- @COMMENT: Hello from the other side
SELECT * 
FROM (
        @Repeat_begin
        SELECT C1 FROM TBL_@Index WHERE ID=@Id
        @Repeat_end
      ) REPEAT;"""

_COMMONS = ['@COMMON1', '@COMMON2']
_IGNORES = ['@Repeat_begin', '@Repeat_end']


class Params:
    def __init__(self, sql):
        self._sql = sql
        self._custom_params = []
        statements = sqlparse.parse(sql)
        for tokens in statements:
            self._find(tokens)

    def _find(self, tokens):
        for token in tokens:
            if token.ttype == sqlparse.tokens.Newline:
                ...
            elif token.ttype == sqlparse.tokens.Punctuation:
                ...
            elif type(token) == sqlparse.sql.Comment:
                ...
            elif token.is_group:
                self._find(token.tokens)
            elif token.ttype == sqlparse.tokens.Name:
                self._add(token)
            elif token.ttype == sqlparse.tokens.String.Single:
                self._add(token)
            elif token.ttype == sqlparse.tokens.Operator:
                self._add(token.parent)

    def _add(self, token):
        founds = re.findall('(@[\w]+)', token.value)
        for val in founds:
            if val not in self._custom_params + _COMMONS + _IGNORES:
                self._custom_params.append(val)

    def getCustomParam(self):
        return self._custom_params


class SimpleGenerator:

    def __init__(self, sql, params_with_value: dict):
        self._sql = sql
        self._params_with_value = params_with_value

        self._statements = []
        statements = sqlparse.parse(sql)
        for tokens in statements:
            self._find(tokens)
            self._statements.append(tokens)

    def _find(self, tokens):
        for token in tokens:
            if token.ttype == sqlparse.tokens.Newline:
                ...
            elif token.ttype == sqlparse.tokens.Punctuation:
                ...
            elif type(token) == sqlparse.sql.Comment:
                ...
            elif token.is_group:
                self._find(token.tokens)
            elif token.ttype == sqlparse.tokens.Name:
                self.replace(token)
            elif token.ttype == sqlparse.tokens.String.Single:
                self.replace(token)
            elif token.ttype == sqlparse.tokens.Operator:
                founds = re.findall('(@[\w]+)', token.parent.value)  # work

    def replace(self, token):
        founds = re.findall('(@[\w]+)', token.value)
        for val in founds:
            token.value = re.sub(val, str(self._params_with_value.get(val)), token.value)

    def get(self):
        return self._statements


_SQL = """select col1, col2, 4000+@col2 from tbl_@COMMON1 WHERE col1='@col1 @col3' and col2=@col2;"""
_PARAMS_WITH_VALUE = {'@COMMON1': 17709, '@col1': 12, '@col2': 40, '@col3': 100}
gen = SimpleGenerator(_SQL, _PARAMS_WITH_VALUE).get()
# print(Params(_SQL).getCustomParam())
print(gen[0])
