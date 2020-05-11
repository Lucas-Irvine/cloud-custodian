# Automatically generated from poetry/pyproject.toml
# flake8: noqa
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['c7n_mailer', 'c7n_mailer.azure_mailer']

package_data = \
{'': ['*'], 'c7n_mailer': ['msg-templates/*']}

install_requires = \
['Jinja2>=2.11,<3.0',
 'boto3>=1.11.12,<2.0.0',
 'datadog>=0.34.0,<0.35.0',
 'jsonpatch>=1.25,<2.0',
 'jsonpointer>=2.0,<3.0',
 'jsonschema>=3.2.0,<4.0.0',
 'ldap3>=2.6.1,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3,<6.0',
 'redis>=3.4.1,<4.0.0',
 'sendgrid>=6.1.1,<7.0.0',
 'splunk-sdk>=1.6.12,<2.0.0']

entry_points = \
{'console_scripts': ['c7n-mailer = c7n_mailer.cli:main',
                     'c7n-mailer-replay = c7n_mailer.replay:main']}

setup_kwargs = {
    'name': 'c7n-mailer',
    'version': '0.6.0',
    'description': 'Cloud Custodian - Reference Mailer',
    'long_description': '# c7n-mailer: Custodian Mailer\n\n[//]: # (         !!! IMPORTANT !!!                    )\n[//]: # (This file is moved during document generation.)\n[//]: # (Only edit the original document at ./tools/c7n_mailer/README.md)\n\nA mailer implementation for Custodian. Outbound mail delivery is still somewhat\norganization-specific, so this at the moment serves primarily as an example\nimplementation.\n\n> The Cloud Custodian Mailer can now be easily run in a Docker container. Click [here](https://hub.docker.com/r/cloudcustodian/mailer) for details.\n\n\n## Message Relay\n\nCustodian Mailer subscribes to an SQS queue, looks up users, and sends email\nvia SES and/or send notification to DataDog. Custodian lambda and instance policies can send to it. SQS queues\nshould be cross-account enabled for sending between accounts.\n\n\n## Tutorial\n\nOur goal in starting out with the Custodian mailer is to install the mailer,\nand run a policy that triggers an email to your inbox.\n\n1. [Install](#developer-install-os-x-el-capitan) the mailer on your laptop (if you are not running as a [Docker container](https://hub.docker.com/r/cloudcustodian/mailer)\n   - or use `pip install c7n-mailer`\n2. In your text editor, create a `mailer.yml` file to hold your mailer config.\n3. In the AWS console, create a new standard SQS queue (quick create is fine).\n   Copy the queue URL to `queue_url` in `mailer.yml`.\n4. In AWS, locate or create a role that has read access to the queue. Grab the\n   role ARN and set it as `role` in `mailer.yml`.\n\nThere are different notification endpoints options, you can combine both.\n\n### Email:\nMake sure your email address is verified in SES, and set it as\n`from_address` in `mailer.yml`. By default SES is in sandbox mode where you\nmust\n[verify](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html)\nevery individual recipient of emails. If need be, make an AWS support ticket to\nbe taken out of SES sandbox mode.\n\nYour `mailer.yml` should now look something like this:\n\n```yaml\nqueue_url: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\nrole: arn:aws:iam::123456790:role/c7n-mailer-test\nfrom_address: you@example.com\n```\n\nYou can also set `region` if you are in a region other than `us-east-1` as well as `lambda_tags` to give the mailer tags.\n\n```yaml\nregion: us-east-2\nlambda_tags:\n  owner: ops\n```\n\nNow let\'s make a Custodian policy to populate your mailer queue. Create a\n`test-policy.yml` file with this content (update `to` and `queue` to match your\nenvironment)\n\n```yaml\n  policies:\n  - name: c7n-mailer-test\n    resource: sqs\n    filters:\n      - "tag:MailerTest": absent\n    actions:\n      - type: notify\n        template: default\n        priority_header: \'2\'\n        subject: testing the c7n mailer\n        to:\n          - you@example.com\n        transport:\n          type: sqs\n          queue: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\n```\n\n### DataDog:\nThe standard way to do a DataDog integration is use the\nc7n integration with AWS CloudWatch and use the\n[DataDog integration with AWS](https://docs.datadoghq.com/integrations/amazon_web_services/)\nto collect CloudWatch metrics. The mailer/messenger integration is only\nfor the case you don\'t want or you can\'t use AWS CloudWatch.\n\nNote this integration requires the additional dependency of datadog python bindings:\n```\npip install datadog\n```\n\nYour `mailer.yml` should now look something like this:\n\n```yaml\nqueue_url: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\nrole: arn:aws:iam::123456790:role/c7n-mailer-test\ndatadog_api_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXX\ndatadog_application_key: YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY\n```\n\n(Also set `region` if you are in a region other than `us-east-1`.)\n\nNow let\'s make a Custodian policy to populate your mailer queue. Create a\n`test-policy.yml`:\n\n```yaml\npolicies:\n  - name: c7n-mailer-test\n    resource: ebs\n    filters:\n     - Attachments: []\n    actions:\n      - type: notify\n        to:\n          - datadog://?metric_name=datadog.metric.name&metric_value_tag=Size\n        transport:\n          type: sqs\n          queue: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\n```\n\nThere is a special `to` format that specifies datadog delivery, and includes the datadog configuration via url parameters.\n- metric_name: is the name of the metrics send to DataDog\n- metric_value_tag: by default the metric value send to DataDog is `1` but if you want to use one of the tags returned in the policy you can set it with the attribute `metric_value_tag`, for example in the `test-policy.yml` the value used is the size of the EBS volume. The value must be a number and it\'s transformed to a float value.\n\n### Slack:\n\nThe Custodian mailer supports Slack messaging as a separate notification mechanism for the SQS transport method. To enable Slack integration, you must specify a Slack token in the `slack_token` field under the `mailer.yml` file.\n\n```yaml\nqueue_url: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\nrole: arn:aws:iam::123456790:role/c7n-mailer-test\nslack_token: xoxo-token123\n```\n\nTo enable Slack messaging, several unique fields are evaluated in the policy, as shown in the below example:\n\n```\npolicies:\n  - name: c7n-mailer-test\n    resource: ebs\n    filters:\n     - Attachments: []\n    actions:\n      - type: notify\n        slack_template: slack\n        to:\n          - slack://owners\n          - slack://foo@bar.com\n          - slack://#custodian-test\n          - slack://webhook/#c7n-webhook-test\n          - slack://tag/resource_tag\n          - https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX\n        transport:\n          type: sqs\n          queue: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\n```\n\nSlack messages support use of a unique template field specified by `slack_template`. This field is unique and usage will not break\nexisting functionality for messages also specifying an email template in the `template` field. This field is optional, however,\nand if not specified, the mailer will use the default value `slack_default`.\n\nSlack integration for the mailer supports several flavors of messaging, listed below. These are not mutually exclusive and any combination of the types can be used, but the preferred method is [incoming webhooks](https://api.slack.com/incoming-webhooks).\n\n| Requires&nbsp;`slack_token` | Key                                                                             | Type   | Notes                                                                                                                                                           |\n|:---------------------------:|:--------------------------------------------------------------------------------|:-------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|\n|             No              | `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX` | string | **(PREFERRED)** Send to an [incoming webhook](https://api.slack.com/incoming-webhooks) (the channel is defined in the webhook)                                  |\n|             Yes             | `slack://owners`                                                                | string | Send to the recipient list generated within email delivery logic                                                                                                |\n|             Yes             | `slack://foo@bar.com`                                                           | string | Send to the recipient specified by email address foo@bar.com                                                                                                    |\n|             Yes             | `slack://#custodian-test`                                                       | string | Send to the Slack channel indicated in string, i.e. #custodian-test                                                                                             |\n|             No              | `slack://webhook/#c7n-webhook-test`                                             | string | **(DEPRECATED)** Send to a Slack webhook; appended with the target channel. **IMPORTANT**: *This requires a `slack_webhook` value defined in the `mailer.yml`.* |\n|             Yes             | `slack://tag/resource-tag`                                                      | string | Send to target found in resource tag. Example of value in tag: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX                    |\n\nSlack delivery can also be set via a resource\'s tag name. For example, using "slack://tag/slack_channel" will look for a tag name of \'slack_channel\', and if matched on a resource will deliver the message to the value of that resource\'s tag:\n\n`slack_channel:https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`\n\nDelivery via tag has been tested with webhooks but should support all delivery methods.\n\n### Splunk HTTP Event Collector (HEC)\n\nThe Custodian mailer supports delivery to the HTTP Event Collector (HEC) endpoint of a Splunk instance as a separate notification mechanism for the SQS transport method. To enable Splunk HEC integration, you must specify the URL to the HEC endpoint as well as a valid username and token:\n\n```yaml\nqueue_url: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\nrole: arn:aws:iam::123456790:role/c7n-mailer-test\nsplunk_hec_url: https://http-inputs-foo.splunkcloud.com/services/collector/event\nsplunk_hec_token: 268b3cc2-f32e-4a19-a1e8-aee08d86ca7f\n```\n\nTo send events for a policy to the Splunk HEC endpoint, add a ``to`` address notify action specifying the name of the Splunk index to send events to in the form ``splunkhec://indexName``:\n\n```\npolicies:\n  - name: c7n-mailer-test\n    resource: ebs\n    filters:\n     - Attachments: []\n    actions:\n      - type: notify\n        to:\n          - splunkhec://myIndexName\n        transport:\n          type: sqs\n          queue: https://sqs.us-east-1.amazonaws.com/1234567890/c7n-mailer-test\n```\n\nThe ``splunkhec://indexName`` address type can be combined in the same notify action with other destination types (e.g. email, Slack, DataDog, etc).\n\n### Now run:\n\n```\nc7n-mailer --config mailer.yml --update-lambda && custodian run -c test-policy.yml -s .\n```\n\nNote: You can set the profile via environment variable e.g. `export AWS_DEFAULT_PROFILE=foo`\n\nYou should see output similar to the following:\n\n```\n(env) $ c7n-mailer --config mailer.yml --update-lambda && custodian run -c test-policy.yml -s .\nDEBUG:custodian.lambda:Created custodian lambda archive size: 3.01mb\n2017-01-12 07:55:16,227: custodian.policy:INFO Running policy c7n-mailer-test resource: sqs region:default c7n:0.8.22.0\n2017-01-12 07:55:16,229: custodian.policy:INFO policy: c7n-mailer-test resource:sqs has count:1 time:0.00\n2017-01-12 07:55:18,017: custodian.actions:INFO sent message:dead-beef policy:c7n-mailer-test template:default count:1\n2017-01-12 07:55:18,017: custodian.policy:INFO policy: c7n-mailer-test action: notify resources: 1 execution_time: 1.79\n(env) $\n```\n\nCheck the AWS console for a new Lambda named `cloud-custodian-mailer`. The\nmailer runs every five minutes, so wait a bit and then look for an email in\nyour inbox. If it doesn\'t appear, look in the lambda\'s logs for debugging\ninformation. If it does, congratulations! You are off and running with the\nCustodian mailer.\n\n\n## Usage & Configuration\n\nOnce [installed](#developer-install-os-x-el-capitan) you should have a\n`c7n-mailer` executable on your path:\naws\n```\n(env) $ c7n-mailer\nusage: c7n-mailer [-h] -c CONFIG\nc7n-mailer: error: argument -c/--config is required\n(env) $\n```\n\nFundamentally what `c7n-mailer` does is deploy a Lambda (using\n[Mu](http://cloudcustodian.io/docs/policy/mu.html)) based on\nconfiguration you specify in a YAML file.  Here is [the\nschema](./c7n_mailer/cli.py#L11-L41) to which the file must conform,\nand here is a description of the options:\n\n| Required? | Key             | Type             | Notes                                                                                                                                                                               |\n|:---------:|:----------------|:-----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| &#x2705;  | `queue_url`     | string           | the queue to listen to for messages                                                                                                                                                 |\n|           | `from_address`  | string           | default from address                                                                                                                                                                |\n|           | `contact_tags`  | array of strings | tags that we should look at for address information                                                                                                                                 |\n\n#### Standard Lambda Function Config\n\n| Required? | Key                  | Type             |\n|:---------:|:---------------------|:-----------------|\n|           | `dead_letter_config` | object           |\n|           | `memory`             | integer          |\n|           | `region`             | string           |\n| &#x2705;  | `role`               | string           |\n|           | `runtime`            | string           |\n|           | `security_groups`    | array of strings |\n|           | `subnets`            | array of strings |\n|           | `timeout`            | integer          |\n\n#### Standard Azure Functions Config\n\n| Required? | Key                   | Type   | Notes                                                                                  |\n|:---------:|:----------------------|:-------|:---------------------------------------------------------------------------------------|\n|           | `function_properties` | object | Contains `appInsights`, `storageAccount` and `servicePlan` objects                     |\n|           | `appInsights`         | object | Contains `name`, `location` and `resourceGroupName` properties                       |\n|           | `storageAccount`      | object | Contains `name`, `location` and `resourceGroupName` properties                       |\n|           | `servicePlan`         | object | Contains `name`, `location`, `resourceGroupName`, `skuTier` and `skuName` properties |\n|           | `name`                | string |                                                                                        |\n|           | `location`            | string | Default: `west us 2`                                                                   |\n|           | `resourceGroupName`   | string | Default `cloud-custodian`                                                              |\n|           | `skuTier`             | string | Default: `Basic`                                                                       |\n|           | `skuName`             | string | Default: `B1`                                                                          |\n\n\n\n\n#### Mailer Infrastructure Config\n\n| Required? | Key                         | Type    | Notes                                                                                                                                                                                              |\n|:---------:|:----------------------------|:--------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n|           | `cache_engine`              | string  | cache engine; either sqlite or redis                                                                                                                                                               |\n|           | `cross_accounts`            | object  | account to assume back into for sending to SNS topics                                                                                                                                              |\n|           | `debug`                     | boolean | debug on/off                                                                                                                                                                                       |\n|           | `ldap_bind_dn`              | string  | eg: ou=people,dc=example,dc=com                                                                                                                                                                    |\n|           | `ldap_bind_user`            | string  | eg: FOO\\\\BAR                                                                                                                                                                                       |\n|           | `ldap_bind_password`        | string  | ldap bind password                                                                                                                                                                                 |\n|           | `ldap_bind_password_in_kms` | boolean | defaults to true, most people (except capone) want to set this to false. If set to true, make sure `ldap_bind_password` contains your KMS encrypted ldap bind password as a base64-encoded string. |\n|           | `ldap_email_attribute`      | string  |                                                                                                                                                                                                    |\n|           | `ldap_email_key`            | string  | eg \'mail\'                                                                                                                                                                                          |\n|           | `ldap_manager_attribute`    | string  | eg \'manager\'                                                                                                                                                                                       |\n|           | `ldap_uid_attribute`        | string  |                                                                                                                                                                                                    |\n|           | `ldap_uid_regex`            | string  |                                                                                                                                                                                                    |\n|           | `ldap_uid_tags`             | string  |                                                                                                                                                                                                    |\n|           | `ldap_uri`                  | string  | eg \'ldaps://example.com:636\'                                                                                                                                                                       |\n|           | `redis_host`                | string  | redis host if cache_engine == redis                                                                                                                                                                |\n|           | `redis_port`                | integer | redis port, default: 6369                                                                                                                                                                          |\n|           | `ses_region`                | string  | AWS region that handles SES API calls                                                                                                                                                              |\n\n#### SMTP Config\n\n| Required? | Key             | Type             | Notes                                                                                                                                                                               |\n|:---------:|:----------------|:-----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n|           | `smtp_server`   | string           | to configure your lambda role to talk to smtpd in your private vpc, see [here](https://docs.aws.amazon.com/lambda/latest/dg/vpc.html) |                                             |\n|           | `smtp_port`     | integer          | smtp port (default is 25)                                                                                                                                                           |\n|           | `smtp_ssl`      | boolean          | this defaults to True                                                                                                                                                               |\n|           | `smtp_username` | string           |                                                                                                                                                                                     |\n|           | `smtp_password` | secured string   |                                                                                                                                                                                     |\n\nIf `smtp_server` is unset, `c7n_mailer` will use AWS SES or Azure SendGrid.\n\n#### DataDog Config\n\n| Required? | Key                       | Type   | Notes                    |\n|:---------:|:--------------------------|:-------|:-------------------------|\n|           | `datadog_api_key`         | string | DataDog API key.         |\n|           | `datadog_application_key` | string | Datadog application key. |\n\nThese fields are not necessary if c7n_mailer is run in a instance/lambda/etc with the DataDog agent.\n\n#### Slack Config\n\n| Required? | Key           | Type   | Notes           |\n|:---------:|:--------------|:-------|:----------------|\n|           | `slack_token` | string | Slack API token |\n\n#### SendGrid Config\n\n| Required? | Key                | Type           | Notes              |\n|:---------:|:-------------------|:---------------|:-------------------|\n|           | `sendgrid_api_key` | secured string | SendGrid API token |\n\n\n#### Splunk HEC Config\n\nThe following configuration items are *all* optional. The ones marked "Required for Splunk" are only required if you\'re sending notifications to ``splunkhec://`` destinations.\n\n| Required for Splunk? | Key                     | Type             | Notes                                                                                                                              |\n|:--------------------:|:------------------------|:-----------------|:-----------------------------------------------------------------------------------------------------------------------------------|\n|       &#x2705;       | `splunk_hec_url`        | string           | URL to your Splunk HTTP Event Collector endpoint                                                                                   |\n|       &#x2705;       | `splunk_hec_token`      | string           | Splunk HEC authentication token for specified username                                                                             |\n|                      | `splunk_remove_paths`   | array of strings | List of [RFC6901](http://tools.ietf.org/html/rfc6901) JSON Pointers to remove from the event, if present, before sending to Splunk |\n|                      | `splunk_actions_list`   | boolean          | If true, add an `actions` list to the top-level message sent to Splunk, containing the names of all non-notify actions taken       |\n|                      | `splunk_max_attempts`   | integer          | Maximum number of times to try POSTing data to Splunk HEC (default 4)                                                              |\n|                      | `splunk_hec_max_length` | integer          | Maximum data length that Splunk HEC accepts; an error will be logged for any message sent over this length                         |\n\n#### SDK Config\n\n| Required? | Key           | Type   | Notes |\n|:---------:|:--------------|:-------|:------|\n|           | `http_proxy`  | string |       |\n|           | `https_proxy` | string |       |\n|           | `profile`     | string |       |\n\n\n#### Secured String\n\nIn order to ensure sensitive data is not stored plaintext in a policy, `c7n-mailer` supports secured\nstrings. You can treat it as a regular `string` or use `secured string` features.\n\n##### AWS\n\nYou can use KMS to encrypt your secrets and use encrypted secret in mailer policy.\nCustodian tries to decrypt the string using KMS, if it fails c7n treats it as a plaintext secret.\n\n```yaml\n    plaintext_secret: <raw_secret>\n    secured_string: <encrypted_secret>\n```\n\n##### Azure\n\nYou can store your secrets in Azure Key Vault secrets and reference them from the policy.\n\n```yaml\n    plaintext_secret: <raw_secret>\n    secured_string:\n        type: azure.keyvault\n        secret: https://your-vault.vault.azure.net/secrets/your-secret\n```\n\nNote: `secrets.get` permission on the KeyVault for the Service Principal is required.\n\n## Configuring a policy to send email\n\nOutbound email can be added to any policy by including the `notify` action.\n\n```yaml\n\npolicies:\n  - name: bad-apples\n    resource: asg\n    filters:\n     - "tag:ASV": absent\n    actions:\n      - type: notify\n        template: default\n        template_format: \'html\'\n        priority_header: \'1\'\n        subject: fix your tags\n        to:\n          - resource-owner\n        owner_absent_contact:\n          - foo@example.com\n        transport:\n          type: sqs\n          queue: https://sqs.us-east-1.amazonaws.com/80101010101/cloud-custodian-message-relay\n```\n\nSo breaking it down, you add an action of type `notify`. You can specify a\ntemplate that\'s used to format the email; customizing templates is described\n[below](#writing-an-email-template).\n\nThe `to` list specifies the intended recipient for the email. You can specify\neither an email address, an SNS topic, a Datadog Metric, or a special value. The special values\nare either\n\n- `resource-owner`, in which case the email will be sent to the listed\n  `OwnerContact` tag on the resource that matched the policy, or\n- `event-owner` for push-based/realtime policies that will send to the user\n  that was responsible for the underlying event.\n- `priority_header` to indicate the importance of an email with [headers](https://www.chilkatsoft.com/p/p_471.asp). Different emails clients will display stars, exclamation points or flags depending on the value. Should be an string from 1 to 5.\n\nBoth of these special values are best effort, i.e., if no `OwnerContact` tag is\nspecified then `resource-owner` email will not be delivered, and in the case of\n`event-owner` an instance role or system account will not result in an email.\n\nThe optional `owner_absent_contact` list specifies email addresses to notify only if\nthe `resource-owner` special option was unable to find any matching owner contact\ntags.\n\nIn addition, you may choose to use a custom tag instead of the default `OwnerContact`.  In order to configure this, the mailer.yaml must be modified to include the contact_tags and the custom tag.  The `resource-owner` will now email the custom tag instead of `OwnerContact`. \n\n```yaml\ncontact_tags:\n  - "custom_tag"\n```\n\n\nFor reference purposes, the JSON Schema of the `notify` action:\n\n```json\n{\n  "type": "object",\n  "required": ["type", "transport", "to"],\n  "properties": {\n    "type": {"enum": ["notify"]},\n    "to": {"type": "array", "items": {"type": "string"}},\n    "owner_absent_contact": {"type": "array", "items": {"type": "string"}},\n    "subject": {"type": "string"},\n    "priority_header": {"type": "string"},\n    "template": {"type": "string"},\n    "transport": {\n      "type": "object",\n      "required": ["type", "queue"],\n      "properties": {\n        "queue": {"type": "string"},\n        "region": {"type": "string"},\n        "type": {"enum": ["sqs"]}\n      }\n    }\n  }\n}\n```\n\n## Using on Azure\n\nRequires:\n\n- `c7n_azure` package.  See [Installing Azure Plugin](https://cloudcustodian.io/docs/azure/gettingstarted.html#azure-install-cc)\n- SendGrid account. See [Using SendGrid with Azure](https://docs.microsoft.com/en-us/azure/sendgrid-dotnet-how-to-send-email)\n- [Azure Storage Queue](https://azure.microsoft.com/en-us/services/storage/queues/)\n\nThe mailer supports an Azure Storage Queue transport and SendGrid delivery on Azure.\nConfiguration for this scenario requires only minor changes from AWS deployments.\n\nYou will need to grant `Storage Queue Data Contributor` role on the Queue for the identity\nmailer is running under.\n\nThe notify action in your policy will reflect transport type `asq` with the URL\nto an Azure Storage Queue.  For example:\n\n```yaml\npolicies:\n  - name: azure-notify\n    resource: azure.resourcegroup\n    description: send a message to a mailer instance\n    actions:\n      - type: notify\n        template: default\n        priority_header: \'2\'\n        subject: Hello from C7N Mailer\n        to:\n          - you@youremail.com\n        transport:\n          type: asq\n          queue: https://storageaccount.queue.core.windows.net/queuename\n```\n\nIn your mailer configuration, you\'ll need to provide your SendGrid API key as well as\nprefix your queue URL with `asq://` to let mailer know what type of queue it is:\n\n```yaml\nqueue_url: asq://storageaccount.queue.core.windows.net/queuename\nfrom_address: you@youremail.com\nsendgrid_api_key: SENDGRID_API_KEY\n```\n\nThe mailer will transmit all messages found on the queue on each execution, and will retry\nsending 3 times in the event of a failure calling SendGrid.  After the retries the queue\nmessage will be discarded.\n\nIn addition, SendGrid delivery on Azure supports using resource tags to send emails. For example, in the `to` field:\n\n```yaml\nto:\n  - tag:OwnerEmail\n```\n\nThis will find the email address associated with the resource\'s `OwnerEmail` tag, and send an email to the specified address.\nIf no tag is found, or the associated email address is invalid, no email will be sent. \n\n#### Deploying Azure Functions\n\nThe `--update-lambda` CLI option will also deploy Azure Functions if you have an Azure\nmailer configuration.\n\n`c7n-mailer --config mailer.yml --update-lambda`\n\nwhere a simple `mailer.yml` using Consumption functions may look like:\n\n```yaml\nqueue_url: asq://storage.queue.core.windows.net/custodian\nfrom_address: foo@mail.com\nsendgrid_api_key: <key>\nfunction_properties:\n  servicePlan:\n    name: \'testmailer1\'\n```\n\n## Writing an email template\n\nTemplates are authored in [jinja2](http://jinja.pocoo.org/docs/dev/templates/).\nDrop a file with the `.j2` extension into the a templates directory, and send a pull request to this\nrepo. You can then reference it in the `notify` action as the `template`\nvariable by file name minus extension. Templates ending with `.html.j2` are\nsent as HTML-formatted emails, all others are sent as plain text.\n\nYou can use `-t` or `--templates` cli argument to pass custom folder with your templates.\n\nThe following variables are available when rendering templates:\n\n| variable          | value                                                        |\n|:------------------|:-------------------------------------------------------------|\n| `recipient`       | email address                                                |\n| `resources`       | list of resources that matched the policy filters            |\n| `event`           | for CWE-push-based lambda policies, the event that triggered |\n| `action`          | `notify` action that generated this SQS message              |\n| `policy`          | policy that triggered this notify action                     |\n| `account`         | short name of the aws account                                |\n| `region`          | region the policy was executing in                           |\n| `execution_start` | The time policy started executing                            |\n\nThe following extra global functions are available:\n\n| signature                                                                    | behavior                                                                                          |\n|:-----------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------|\n| `format_struct(struct)`                                                      | pretty print a json structure                                                                     |\n| `resource_tag(resource, key)`                                                | retrieve a tag value from a resource or return an empty string, aliased as get_resource_tag_value |\n| `format_resource(resource, resource_type)`                                   | renders a one line summary of a resource                                                          |\n| `date_time_format(utc_str, tz_str=\'US/Eastern\', format=\'%Y %b %d %H:%M %Z\')` | customize rendering of an utc datetime string                                                     |\n| `search(expression, value)`                                                  | jmespath search value using expression                                                            |\n| `yaml_safe(value)`                                                           | yaml dumper                                                                                       |\n\nThe following extra jinja filters are available:\n\n| filter                                                                                         | behavior                                                                                                                                                                                      |\n|:-----------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| <code>utc_string&#124;date_time_format(tz_str=\'US/Pacific\', format=\'%Y %b %d %H:%M %Z\')</code> | pretty [format](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior) the date / time                                                                                   |\n| <code>30&#124;get_date_time_delta</code>                                                       | Convert a time [delta](https://docs.python.org/2/library/datetime.html#datetime.timedelta) like \'30\' days in the future, to a datetime string. You can also use negative values for the past. |\n\n\n## Developer Install (OS X El Capitan)\n\nClone the repository:\n```\n$ git clone https://github.com/cloud-custodian/cloud-custodian\n```\nInstall dependencies (with virtualenv):\n```\n$ virtualenv c7n_mailer\n$ source c7n_mailer/bin/activate\n$ cd tools/c7n_mailer\n$ pip install -r requirements.txt\n```\nInstall the extensions:\n```\npython setup.py develop\n```\n\n## Testing Templates and Recipients\n\nA ``c7n-mailer-replay`` entrypoint is provided to assist in testing email notifications\nand templates. This script operates on an actual SQS message from cloud-custodian itself,\nwhich you can either retrieve from the SQS queue or replicate locally. By default it expects\nthe message file to be base64-encoded, gzipped JSON, just like c7n sends to SQS. With the\n``-p`` | ``--plain`` argument, it will expect the message file to contain plain JSON.\n\n``c7n-mailer-replay`` has three main modes of operation:\n\n* With no additional arguments, it will render the template specified by the policy the\n  message is for, and actually send mail from the local machine as ``c7n-mailer`` would.\n  This only works with SES, not SMTP.\n* With the ``-T`` | ``--template-print`` argument, it will log the email addresses that would\n  receive mail, and print the rendered message body template to STDOUT.\n* With the ``-d`` | ``--dry-run`` argument, it will print the actual email body (including headers)\n  that would be sent, for each message that would be sent, to STDOUT.\n  \n#### Testing Templates for Azure\n\nThe ``c7n-mailer-replay`` entrypoint can be used to test templates for Azure with either of the arguments:\n* ``-T`` | ``--template-print`` \n* ``-d`` | ``--dry-run`` \n  \nRunning ``c7n-mailer-replay`` without either of these arguments will throw an error as it will attempt\nto authorize with AWS. \n\nThe following is an example for retrieving a sample message to test against templates:\n\n* Run a policy with the notify action, providing the name of the template to test, to populate the queue.\n\n* Using the azure cli, save the message locally: \n```\n$ az storage message get --queue-name <queuename> --account-name <storageaccountname> --query \'[].content\' > test_message.gz\n```\n* The example message can be provided to ``c7n-mailer-replay`` by running:\n\n```\n$ c7n-mailer-replay test_message.gz -T --config mailer.yml\n```\n',
    'long_description_content_type': 'text/markdown',
    'author': 'Cloud Custodian Project',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cloudcustodian.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
