# Week 0 — Billing and Architecture

### Install AWS CLI
```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Check that the AWS CLI is working and you are the expected user
```sh
aws sts get-caller-identity
```

You should see something like this:
```json
{
    "UserId": "AIDAQEIP3PTMKHCDS3C7M",
    "Account": "009160064216",
    "Arn": "arn:aws:iam::009160064216:user/mjolsen"
}
```

#### Create Alarm
- [aws cloudwatch put-metric-alarm](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-alarm.html)
- [Create an Alarm via AWS CLI](https://aws.amazon.com/premiumsupport/knowledge-center/cloudwatch-estimatedcharges-alarm/)
- We need to update the configuration json script with the TopicARN we generated earlier
- We are just a json file because --metrics is is required for expressions and so its easier to us a JSON file.

```sh
aws cloudwatch put-metric-alarm --cli-input-json file://aws/json/alarm_config.json
```