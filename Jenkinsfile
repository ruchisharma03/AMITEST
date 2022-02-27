//  store 'region': 'latest ami is present or not'
def serviceAmiIdChanged = [: ]
String cron_string = "0 0 */20 * *" // cron every 20th of the month

pipeline {
  agent none
  // triggers {
  //   cron(cron_string)
  // }
  parameters {

    string(name: 'AWS_AGENT_LABEL', defaultValue: 'any', description: 'Label of the Agent which has python3 and aws profile configured')
    string(name: 'AWS_SERVICE_CONFIG_FILE', defaultValue: './config/config.json', description: 'Path of the aws service config file')
    string(name: 'JOB_NAMES', description: 'List of jobs separated by commas in build sequence (job names for the service).')
    string(name: 'API_TOKEN', description: 'Token for Jira tickets).')
  }

  stages {
    stage('check the ami version') {
      agent {label "${AWS_AGENT_LABEL}"}
      steps {
        
        stash includes: '**', name: 'jiraSource'
          script {

            def result = sh(returnStdout: true, script: 'python3 check_ami_version.py')
            println(result);

            for (String jobStatus: result.split(',')) {

              String[] eachjobStatus = jobStatus.split(':');

              if (eachjobStatus.size() > 1) {

                serviceAmiIdChanged[eachjobStatus[0]] = eachjobStatus[1];
              }

            }
          }
        }
    }
    // create the jobs dynamically
    stage('build the QA services if the latest ami id is present') {

      steps {
        

        script {

          String[] jobList = params.JOB_NAMES.split(',');
          println(jobList[0])
          println(serviceAmiIdChanged[jobList[0]])
          if (jobList.size() > 0) {

            for (String eachJob: jobList) {
              
              if (serviceAmiIdChanged[eachJob] == 'True') {
                try {
                  stage("QA-${eachJob}") {

                    build job: "${eachJob}", wait: true
                    // emailext body: "${eachJob} succeeded", recipientProviders: [buildUser()], subject: "JOB ${eachJob} SUCCESS", to: ''

                  }
                } catch (Exception e) {

                  echo "${eachJob} failed"
                  // emailext body: "${eachJob} failed", recipientProviders: [buildUser()], subject: "JOB ${eachJob} FAILED", to: ''
                  throw e;

                }

              }

            }

          }

        }
      }

    }

  }

  post {
    always {
      echo "====++++always++++===="
    }
    success {
      echo "====++++only when successful ++++===="
      node("${AWS_AGENT_LABEL}"){
        withCredentials([[
            $class: 'UsernamePasswordMultiBinding',
            credentialsId: "jira-cred",
            usernameVariable: 'JIRA_USERNAME',
            passwordVariable: 'JIRA_API_TOKEN',
        ]]) {
            
            unstash "jiraSource"
            sh """
              ls -l
              python3 jira_scripts/create_issue.py
              """
        }

      }
    }
    failure {
      echo "====++++only when failed++++===="
    }
  }

}
