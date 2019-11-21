#!groovy

pipeline{
    agent {
        docker {
            image 'python:3.7.4'
            args '-u root'
        }
    }
    environment {
        CODACY_PROJECT_TOKEN = credentials('codacy-coco-secretsmanager')
    }
    triggers {
        pollSCM 'H/10 * * * *'
    }
    options {
        skipDefaultCheckout false
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }
    stages{
        stage('Coverage to Codacy'){
            steps {
                slackSend (color: 'good', message: "datacoco_secretsmanager_pypi_pipeline_${GIT_BRANCH} - Starting build #${BUILD_NUMBER}. (<${env.BUILD_URL}|Open>)")

                echo "coverage"
           
                // sh "pip install -r requirements.txt"
                // sh "pip install coverage codacy-coverage"
                // sh "coverage run -m unittest tests/test_secrets.py"
                // sh "coverage xml -i"
                // sh "python-codacy-coverage -r coverage.xml"
            }
            post {
                always {
                    echo "plugin"
                    // step([$class: 'CoberturaPublisher',
                    //                autoUpdateHealth: false,
                    //                autoUpdateStability: false,
                    //                coberturaReportFile: 'coverage.xml',
                    //                failNoReports: false,
                    //                failUnhealthy: false,
                    //                failUnstable: false,
                    //                maxNumberOfBuilds: 10,
                    //                onlyStable: false,
                    //                sourceEncoding: 'ASCII',
                    //                zoomCoverageChart: false])
                }
            }       
        }
        stage('Deploy to Pypi') {   
            steps {

                withCredentials([[
                    $class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'e9f73e25-ab88-4382-9018-dd0841cc327c',
                    usernameVariable: 'USERNAME',
                    passwordVariable: 'PASSWORD'
                ]]) {
                    sh "pip install twine"
                    sh "rm -rf dist"
                    sh "python setup.py sdist"
                    sh "twine upload --repository-url https://test.pypi.org/legacy/ --skip-existing dist/* -u ${USERNAME} -p ${PASSWORD}"
                    // sh "twine upload --skip-existing dist/* -u ${USERNAME} -p ${PASSWORD}"
                }
            }
        }
    }
    post {
        failure {
            echo "fail"
            slackSend (color: 'danger', message: "@here datacoco_secretsmanager_pypi_pipeline_${GIT_BRANCH} - Build #${BUILD_NUMBER} Failed. (<${env.BUILD_URL}|Open>)")
        }
        success {
            echo "good"
            slackSend (color: 'good', message: "datacoco_secretsmanager_pypi_pipeline_${GIT_BRANCH} - Build #${BUILD_NUMBER} Success. (<${env.BUILD_URL}|Open>)")
        }
        always {
            echo 'Updating folder permissions.'
            sh "chmod -R 777 ."
        }
        cleanup {
            echo 'Workspace cleanup.'
            deleteDir()
        }
    }
}