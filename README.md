# Minio docker example
Just a poc how works webhooks on Minio
## Installation

```
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements

docker compose up

```

Wait a seconds/minutes to pull/build/run container and check if minio is ready on http://localhost:5091 and execute script available in poc-minio/minio/setup/configure-minio.sh

## User with access limited to a specific bucket

Configure alias:

```
mc alias set minio http://localhost:9000 admin password
```

Create a user:

```
mc admin user add minio theuser thepass12345678
```

Create a policy file named `intake-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::intake",
        "arn:aws:s3:::intake/*"
      ]
    }
  ]
}

```

Apply policy:

```
mc admin policy create minio intake-policy intake-policy.json
```

Assign intake policy to user:

```
mc admin policy attach minio intake-policy --user theuser
```

List of all alias configured:

```
mc alias list
```

List all users:

```
mc admin user list minio
```

List all policies:

```
mc admin policy list minio
```

View user details:

```
mc admin user info minio USER_NAME
```

View policy details:

```
mc admin policy info minio POLICY_NAME
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

If you use this code, please include attribution to this project.

---
<!-- Pit i Collons -->
<!--
https://youtu.be/E9de-cmycx8?si=e07Xq20kSNc9idGb
-->
![Coded In Barcelona](https://raw.githubusercontent.com/leguim-repo/leguim-repo/master/img/currentfooter.png)