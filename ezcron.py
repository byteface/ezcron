# -*- coding: utf-8 -*-
import calendar
import re
from datetime import datetime
from html import escape

from sanic import Sanic
from sanic import response
from domonic.terminal import crontab, date, uptime
from domonic.javascript import Global
from domonic.html import *
from domonic import domonic
from cron_descriptor import Options, ExpressionDescriptor
from croniter import croniter

from app import *

# this gets populated with parsed lines on page refresh
_crons = {}

# settings for cron_descriptor
_options = Options()
_options.day_of_week_start_index_zero = False
_options.use_24hour_time_format = True


class CrontabRenderer(object):

    rex = re.compile(r"^(\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}).+$")
    
    def __init__(self, ctab_data):
        self.ctab_data = ctab_data
        self.count = 0
        _crons = {}
        self.__call__() # just to force the count

    def __call__(self):
        self.count = 0
        output=""
        lines = self.ctab_data.split('\n')
        for line_number, line in enumerate(lines):
            parsed_line, parsed_command = self.parse_cron_line(line)
            if parsed_line:
                self.count += 1
                _crons[str(line_number)] = parsed_command
                output = output + self.print_line(parsed_line, parsed_command, line_number)
                output = output + self.create_modal(parsed_line, parsed_command)
        return output

    def get_next(self, pcron):
        iter = croniter(pcron, datetime.datetime.now())  # TODO - timezone offset
        return str(iter.get_next(datetime.datetime))

    def print_line(self, parsed_line, parsed_command, line_number):
        hex = self.random_color()
        ref = 'modal_'+str(self.count) # the target modal
        return str(
                div(
                strong( parsed_line, _style=f'color:{hex};', _class="thecron"),
                " Runs: " + str(ExpressionDescriptor(parsed_line, _options)),
                " ", pre( escape(parsed_command) ),
                " ",button( "✏️ EDIT", **{'_data-ref':ref}, _class='open btn-sm' ),
                " ",button( "X DELETE", _class='del btn-sm', **{'_data-ref':ref}, _onclick="alert('Not Yet Implmented!');" ),
                " ",button( "🏃 RUN NOW", _class='go btn-sm', **{'_data-ref':ref}, _onclick=f"run_job({line_number})"),
                div( "Next one will run at : "+self.get_next(parsed_line) ),
                strong( "Countdown:" ),
                div( _id="countdown"+str(self.count) ),
                # notice im changing the js interval var dynamicaly by appending the count to the id
                script(f'const timer{str(self.count)} = setInterval(showRemaining, 1000, "{self.get_next(parsed_line)}", "countdown{str(self.count)}", "timer{str(self.count)}" );'),
                hr()
                )
            )

    def create_modal(self, pcron, parsed_command):
        # explanation of parts you can use
        parts = table(
                tbody(
                    tr(th('*'), td("any value")),
                    tr(th(','), td("value list separator")),
                    tr(th('-'), td("range of values")),
                    tr(th('/'), td("step values")),
                    tr(th('0-9'), td("numbers"))
                ), _style="padding:0px;"
            )

        return str(Modal("modal_"+str(self.count), div(
            strong('explanation:'),
            div(ExpressionDescriptor(pcron, _options), _id="hr"+str(self.count), _class="human-readable"),
            strong('cron:'),
            input(_class="in_cron", _id="in_cron"+str(self.count), _type="text", _value=pcron),
            strong('command:'),
            input(_id="in_comm"+str(self.count), _type="text", _value=escape(parsed_command)),
            parts,
            button("Save"),
            button("Cancel", _class="del"),
            _class="text-editor"
            )
        ))

    def random_color(self):
        import random
        r = lambda: random.randint(0,255)
        return str('#%02X%02X%02X' % (r(),r(),r()))

    def parse_cron_line(self, line):
        stripped = line.strip()
        if stripped and stripped.startswith('#') is False:
            rexres = self.rex.search(stripped)
            if rexres:
                code = ' '.join(rexres.group(1).split())
                command = ''.join(stripped.split(code))
                command = command.strip()
                return code, command
        return None, None


app = Sanic(name='ezcron')
app.static('/assets', './assets')

# give it a cron. returns div containing human readable
@app.route('/cron_description')
async def cron_description(request):
    readable = ExpressionDescriptor(request.args['cron'][0], _options)
    return response.html( str(div(readable, _id=f"{request.args['id'][0]}", _class="human-readable")) )

@app.route('/run_job')
async def cron_description(request):
    ctab = CrontabRenderer(str(crontab("-l")))  # refresh them.
    cmd = _crons[request.args['line'][0]]
    from domonic.terminal import command
    command.run( cmd )
    return response.html( "done" )

@app.route('/create')
async def cron_create(request):
    # get the cron. and the script. append to file
    return response.html( "done" )

@app.route('/update')
async def cron_update(request):
    # replace line
    return response.html( "done" )

@app.route('/delete')
async def cron_delete(request):
    # remove line    
    return response.html( "done" )

@app.route('/')
async def home(request):

    ctab = CrontabRenderer(str(crontab("-l")))
    # last_edit = str(crontab("-v")) # try/catch

    htmlcal = calendar.HTMLCalendar(calendar.SUNDAY)
    cal = htmlcal.formatyear(2020,1)
    upt = str(uptime())
    page = article(
        script(_src="/assets/js/later.min.js"),
        script(_src=domonic.JS_MASTER),
        link(_rel="stylesheet", _type="text/css", _href=domonic.CSS_STYLE),
        div(
            sub(str(date()), " ", a("🔄", _href="/")),
            h1("📅 ezcron"),
            _style="text-align:center;"
        ),
        div(
            div(ExpressionDescriptor("* * * * *", _options), _id="hr0", _class="human-readable"),
            input(_class="in_cron", _id="in_cron0", _type="text", _value="* * * * *"),
            _class="cron-input"
        ),
        h5(f"{ctab.count} cron jobs detected:"),
        div(str(ctab())),
        button("Add another"),
        h5("When the cron jobs are scheduled to run:"),
        div(cal),
        p(strong("uptime : "), upt),
        h5("Useful Links:"),
        a( "crontab guru", _href="https://crontab.guru/", _target="_blank")
        )

    return response.html( render( Webpage(page) ) )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
