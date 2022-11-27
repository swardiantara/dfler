import pdfkit
import json
from datetime import datetime
import os
import sys
import pandas as pd
# import dfler from output_dir


def build_head():
  print("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Forensic Report</title>
  </head>
  """)

def build_foot():
  print("""
    </body>
  <footer id="footer">
    <span class="timestamp"> <em>Generated using dfler v.0.1</em> </span>
  </footer>
</html>
  """)


def build_style():
  print("""
  <style>
    body {
      font-family: Arial, Helvetica, sans-serif;
    }
    .text-center {
      text-align: center;
    }
    th {
      text-align: center;
    }

    th,
    td {
      padding-top: 5px;
      padding-bottom: 5px;
      padding-left: 8px;
      padding-right: 8px;
    }

    /* table,
    th,
    td {
      border: 1px solid #000;
    } */

    .timeline {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 1.2em;
      text-align: center;
      font-weight: bold;
    }

    table.fixed {
      table-layout: fixed;
    }
    table.fixed td {
      overflow: hidden;
    }

    table {
      border-collapse: collapse;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.95em;
    }

    table.table-timeline {
      width: 100%;
      font-size: 1em;
    }
    table.table-timeline,
    table.table-timeline > thead > tr > th,
    table.table-timeline > tbody > tr > td {
      border: 1px solid #000;
    }

    table.table-timeline > thead > tr > th {
      font-weight: bold;
    }

    table.table-timeline > tbody > tr > td:first-child {
      text-align: center;
    }

    .outside {
      color: #000;
    }

    .issue {
      color: red;
    }

    .parameter {
      color: coral;
    }

    .action {
      color: rgb(185, 0, 0);
    }

    .component {
      color: blue;
    }

    .function {
      color: blueviolet;
    }

    .state {
      color: #009eff;
    }

    .bold {
      text-emphasis-color: red;
    }

    #footer {
      margin-top: 7px;
      display: flex;
      justify-content: space-between;
    }

    .content-color {
      color: #2b4f60;
    }

    .timestamp {
      color: grey;
      font-size: small;
    }
    .page-number {
      width: 50%;
      text-align: right;
      margin-right: 5px;
    }

    .report-title {
      font-weight: bold;
      text-align: left;
      font-size: 1.8em;
      color: #0e5e6f;
    }

    .title-color {
      color: #0e5e6f;
      font-size: 1em;
    }

    #metadata {
      margin-top: 3em;
    }

    #table-metadata {
      border: none !important;
      width: 30%;
      font-size: 1em;
      margin-left: -8px;
    }

    #color-legend.table-timeline {
      width: 9%;
      border: none !important;
    }

    .box {
      float: left;
      width: 20px;
      height: 20px;
      margin: 5px;
      border: 1px solid rgba(0, 0, 0, 0.2);
    }

    .outside-box {
      background: #000;
    }

    .issue-box {
      background: red;
    }

    .parameter-box {
      background: coral;
    }

    .action-box {
      background: rgb(185, 0, 0);
    }

    .component-box {
      background: blue;
    }

    .function-box {
      background: blueviolet;
    }

    .state-box {
      background: #009eff;
    }

    .break-before {
      page-break-before: always;
    }
  </style>
  """)


def build_report_header():
  print("""
  <body>
    <h4 class="report-title">Drone Forensic Report</h4>
    <hr style="margin-top: -2em" />
    <span class="timestamp"
      >This report is generated on: 11/15/2022 21:45:53</span
    >
    <section id="metadata">
      <table id="table-metadata fixed">
        <col width="30%" />
        <col width="70%" />
        <tr>
          <td>Computer Name</td>
          <td>Swardiantara</td>
        </tr>
        <tr>
          <td>Report Type</td>
          <td>Entity Recognition</td>
        </tr>
        <tr>
          <td>Number of log files</td>
          <td>12</td>
        </tr>
      </table>
    </section>
  """)


def build_source_evidence(config):
  print("""
    <section>
      <h4 class="title-color" style="margin-top: 3em">Source evidence</h4>
      <hr style="margin-top: -1em" />
      <ul class="content-color">
        <li>DJIFlightRecord_2018-06-15_(11-17-44).csv</li>
        <li>DJIFlightRecord_2018-06-15_(11-17-44).csv</li>
        <li>DJIFlightRecord_2018-06-15_(11-17-44).csv</li>
        <li>14-045b34780500a6629d11a9560a89579381fcaa6b</li>
        <li>14-045b34780500a6629d11a9560a89579381fcaa6b</li>
        <li>14-045b34780500a6629d11a9560a89579381fcaa6b</li>
      </ul>
    </section>
  """)


def build_ner_result():
  print("""
    <section>
      <h4 class="title-color" style="margin-top: 3em">Recognition Results</h4>
      <hr style="margin-top: -1em" />
      <table id="table-metadata fixed">
        <col width="40%" />
        <col width="10%" />
        <col width="40%" />
        <col width="10%" />
        <tr>
          <td>Number of messages</td>
          <td>172</td>
          <td>Number of token</td>
          <td>1550</td>
        </tr>
        <tr>
          <td>Number of entitiy</td>
          <td>1092</td>
          <td>Number of non-entitiy</td>
          <td>458</td>
        </tr>
        <tr>
          <td>Number of state entity</td>
          <td>29</td>
          <td>Number of issue entity</td>
          <td>102</td>
        </tr>
        <tr>
          <td>Number of action entity</td>
          <td>32</td>
          <td>Number of function entity</td>
          <td>100</td>
        </tr>
        <tr>
          <td>Number of component entity</td>
          <td>71</td>
          <td>Number of parameter entity</td>
          <td>124</td>
        </tr>
      </table>
    </section>
  """)

def build_th():
  print("""
  <section class="break-before">
    <h5 class="timeline">Highlights Color Code</h5>
      <table class="table-timeline fixed">
        <col width="10%" />
        <col width="20%" />
        <col width="70%" />
        <thead>
          <tr>
            <th>Color Code</th>
            <th>Entity Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
                    <tr>
            <td>
              <span class="box issue-box"></span>
            </td>
            <td>
              <span class="issue">Issue</span>
            </td>
            <td>
              Words/phrases that indicate some issues happen to the drone.
            </td>
          </tr>
          <tr>
            <td>
              <span class="box parameter-box"></span>
            </td>
            <td>
              <span class="parameter">Parameter</span>
            </td>
            <td>
              Words/phrases that represent some parameters of configuration in a
              drone.
            </td>
          </tr>
          <tr>
            <td>
              <span class="box action-box"></span>
            </td>
            <td>
              <span class="action">Action</span>
            </td>
            <td>
              Words/phrases that indicate some actions taken by the drone.
            </td>
          </tr>
          <tr>
            <td>
              <span class="box component-box"></span>
            </td>
            <td><span class="component">Component</span></td>
            <td>Words/phrases that reflect physical components of a drone</td>
          </tr>
          <tr>
            <td>
              <span class="box function-box"></span>
            </td>
            <td><span class="function">Function</span></td>
            <td>
              Words/phrases that denote some functionalities or features of a
              drone equipped with.
            </td>
          </tr>
          <tr>
            <td>
              <span class="box state-box"></span>
            </td>
            <td><span class="state">State</span></td>
            <td>
              Words/phrases that notify a state/mode of a drone operates in
              during a flight.
            </td>
          </tr>
        </tbody>
      </table>
      <h5 class="timeline" style="margin-top: 3em">
        Highlighted Forensic Timeline
      </h5>
      <table class="table-timeline fixed">
        <col width="30%" />
        <col width="70%" />
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
      """)


def build_tf():
  print("""
        </tbody>
      </table>
    </section>
  """)


def statistics(config, ner_result):
  entities_json = open('./flight_logs/entities.json')
  entities = json.load(entities_json)

  word_list = []
  tag_list = []
  for record in entities:
      timestamp = record['timestamp']
      messages = record['entities']
      for message in messages:
          for word, tag in message.items():
              word_list.append(word)
              tag_list.append(tag)

  ner_result = pd.DataFrame(list(zip(word_list, tag_list)), columns =['word', 'tag'])
  entity_df = ner_result[ner_result['tag'] != 'O']
  non_entity_df = ner_result[ner_result['tag'] == 'O']
  issue = ['B-ISSUE', 'I-ISSUE']
  issue_df = ner_result[ner_result['tag'].isin(issue)]
  component = ['B-COMPONENT', 'I-COMPONENT']
  component_df = ner_result[ner_result['tag'].isin(component)]
  action = ['B-ACTION', 'I-ACTION']
  action_df = ner_result[ner_result['tag'].isin(action)]
  parameter = ['B-PARAMETER', 'I-PARAMETER']
  parameter_df = ner_result[ner_result['tag'].isin(parameter)]
  state = ['B-STATE', 'I-STATE']
  state_df = ner_result[ner_result['tag'].isin(state)]
  function = ['B-FUNCTION', 'I-FUNCTION']
  function_df = ner_result[ner_result['tag'].isin(function)]

  return {
    'message': len(entities),
    'entity': len(entity_df),
    'non_entity': len(non_entity_df),
    'issue': len(issue_df),
    'component': len(component_df),
    'action': len(action_df),
    'parameter': len(parameter_df),
    'state': len(state_df),
    'function': len(function_df),
  }


def build_forensic_table(config):
  # Opening JSON file
  timeline_file = open(config['output_dir'] + '/ner_result.json')
  timeline = json.load(timeline_file)
  
  build_th()
  # Loop the table
  build_tr(timeline)
  # Closing file
  build_tf()
  timeline_file.close()


def build_tr(records):
  for record in records:
    timestamp = record['timestamp']
    print("""
      <tr>
        <td>{timestamp}</td>
        <td>
    """.format(timestamp=timestamp))
    messages = record['entities']
    for message in messages:
      for word, tag in message.items():
        if tag == 'O':
          # generate tag span O
          print("""<span class="{tag}">{token}</span>""".format(tag='outside', token=word))
        elif tag == 'B-ISSUE' or tag == 'I-ISSUE':
          print("""<span class="{tag}">{token}</span>""".format(tag='issue', token=word))
        elif tag == 'B-PARAMETER' or tag == 'I-PARAMETER':
          print("""<span class="{tag}">{token}</span>""".format(tag='parameter', token=word))
        elif tag == 'B-ACTION' or tag == 'I-ACTION':
          print("""<span class="{tag}">{token}</span>""".format(tag='action', token=word))
        elif tag == 'B-COMPONENT' or tag == 'I-COMPONENT':
          print("""<span class="{tag}">{token}</span>""".format(tag='component', token=word))
        elif tag == 'B-FUNCTION' or tag == 'I-FUNCTION':
          print("""<span class="{tag}">{token}</span>""".format(tag='function', token=word))
        elif tag == 'B-STATE' or tag == 'I-STATE':
          print("""<span class="{tag}">{token}</span>""".format(tag='state', token=word))
      
    print("""
        </td>
      </tr>
    """)

def statistical_analysis(config):
  # Opening JSON file
  ner_result = open(config['output_dir'] + '/ner_result.json')
  ner_result = json.load(ner_result)

def build_html(config, filename):
  output_dir = config['output_dir']
  full_path = os.path.join(output_dir, filename + ".html")

  sys.stdout = open(full_path, 'w')
  build_head()
  build_style()
  build_report_header()
  build_source_evidence(config)
  build_ner_result(config)
  build_forensic_table()
  build_foot()
  sys.stdout.close()


def generatePDF(config, filename):
  # Define path to wkhtmltopdf.exe
  # path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
  path_to_wkhtmltopdf = config['wkhtml_path']
  # Define path to input and output file
  output_dir = config['output_dir']
  full_path = os.path.join(output_dir, filename)
  # Point pdfkit configuration to wkhtmltopdf.exe
  config_wkhtml = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
  # Convert HTML file to PDF
  pdfkit.from_file(full_path + ".html", output_path = full_path + ".pdf", configuration=config_wkhtml)


def generate_report(config):
  # Prepare the filename and outputdir
  # Move to the config, so that every function can access
  # now = datetime.now()
  # now = now.strftime("%d%m%Y_%H%M%S")
  # output_dir = os.path.join("./result", now)
  filename = "forensic_report_"

  build_html(config, filename)
  generatePDF(config, filename)
    