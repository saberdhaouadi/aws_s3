!/bin/bash
while read -r account_name account;
do
    OUT=$(aws sts assume-role --role-arn arn:aws:iam::$account:role/CostControlDashboard --role-session-name $account_name) ;
      export AWS_ACCESS_KEY_ID=$(echo $OUT | jq -r '.Credentials''.AccessKeyId');
      export AWS_SECRET_ACCESS_KEY=$(echo $OUT | jq -r '.Credentials''.SecretAccessKey');
      export AWS_SESSION_TOKEN=$(echo $OUT | jq -r '.Credentials''.SessionToken');
      aws sts get-caller-identity | jq -r '.UserId';


      aws s3api list-buckets --region "us-east-1"





   unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
done < account_list


