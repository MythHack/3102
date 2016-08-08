#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re
from textwrap import dedent
from template import Output


class OutputHtml(Output):

    def save(self, output_file):
        super(OutputHtml, self).save(output_file)
        html = self._html_generate()
        with open(output_file, 'w') as f:
            f.write(html)

    def _html_generate(self):
        td_dict = {}
        td_piece = th_str = ''
        for key in self.keys:
            td_piece += ' <td>{{ %s }}</td> ' % key
            th_str += ' <th>%s</td> ' % key
        td = '<tr>%s</tr>' % td_piece

        tables = ''
        self._table_base = dedent(self._table_base)
        self._html_base = dedent(self._html_base)
        for key in ['root_domain', 'ip', 'domain']:
            for item in self.result[key].values():
                group = td_dict.setdefault(item['module'], [])
                group.append(item)
        for item in td_dict:
            td_str = '\n'.join(
                [self._generate_key(td, _) for _ in td_dict[item]]
            )
            tables += self._table_base % (
                self._reindent(th_str, 4), self._reindent(td_str, 4)
            )
        html = self._html_base % self._reindent(tables, 16)
        return html

    def _generate_key(self, template, context):
        content = template
        for key in self._extract_vars(template):
            if key not in context:
                error_msg = "%s is missing from the template context" % key
                raise ValueError(error_msg)
            content = content.replace("{{ %s }}" % key, str(context[key]))
        return content

    def _extract_vars(self, template):
        keys = set()
        for match in re.finditer(r"\{\{ (?P<key>\w+) \}\}", template):
            keys.add(match.groups()[0])
        return sorted(list(keys))

    def _reindent(self, s, num_space):
        leading_space = num_space * ' '
        lines = [leading_space + line for line in s.splitlines()]
        return '\n'.join(lines)

    _table_base = """\
    <thead>
    %s
    </thead>
    <tbody>
    %s
    </tbody>
    """

    _html_base = """\
    <!DOCTYPE html>
    <html lang="zh-cn">
        <head>
            <meta charset="utf-8">
            <title></title>
            <style type="text/css">
            caption{padding-top:8px;padding-bottom:8px;color:#777;text-align:left}th{text-align:left}.table{width:100%%;max-width:100%%;margin-bottom:20px}.table>thead>tr>th,.table>tbody>tr>th,.table>tfoot>tr>th,.table>thead>tr>td,.table>tbody>tr>td,.table>tfoot>tr>td{padding:8px;line-height:1.42857143;vertical-align:top;border-top:1px solid #ddd}.table>thead>tr>th{vertical-align:bottom;border-bottom:2px solid #ddd}
            </style>
        </head>
        <body>
            <div class="container">
                <table class="table">
    %s
                </table>
            </div>
        </body>
    </html>
    """
