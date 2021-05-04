terraform {
  required_version = "~>0.13"
  backend "s3" {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "diegorocha.com.br/terraform.tfstate"
    region               = "us-east-1"
    profile              = "diego"
  }
}

resource "aws_s3_bucket" "bucket_staticfiles" {
  bucket = "diegorocha-static"
  acl    = "private"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = [
      "https://diegorocha.com.br",
      "https://www.diegorocha.com.br",
      "http://localhost:8000"
    ]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    service = "diegorocha.com.br"
    backup  = "false"
  }
}

resource "aws_s3_bucket_policy" "bucket_staticfiles_policy" {
  bucket = aws_s3_bucket.bucket_staticfiles.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action = [
          "s3:GetObject",
        ]
        Resource = [
          "${aws_s3_bucket.bucket_staticfiles.arn}/*"
        ]
      },
    ]
  })
}

resource "aws_iam_policy" "policy_diegorocha_com_br_s3" {
  name        = "policy_diegorocha_com_br_s3"
  path        = "/"
  description = "Policy to allow read/write to ${aws_s3_bucket.bucket_staticfiles.bucket} bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObjectAcl",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Resource = [
          aws_s3_bucket.bucket_staticfiles.arn,
          "${aws_s3_bucket.bucket_staticfiles.arn}/*"
        ]
      },
    ]
  })
}

resource "aws_ecr_repository" "ecr_repository" {
  name                 = "diegorocha"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    service = "diegorocha.com.br"
  }
}

resource "aws_ecr_lifecycle_policy" "ecr_repository_lifecycle" {
  repository = aws_ecr_repository.ecr_repository.name

  policy = jsonencode(
    {
      rules = [
        {
          action = {
            type = "expire"
          }
          description  = "Keep last 3 images"
          rulePriority = 1
          selection = {
            countNumber = 3
            countType   = "imageCountMoreThan"
            tagStatus   = "any"
          }
        },
      ]
    }
  )
}

output "diegorocha_bucket_name" {
  value = aws_s3_bucket.bucket_staticfiles.bucket
}

output "diegorocha_policies_arn" {
  value = [
    aws_iam_policy.policy_diegorocha_com_br_s3.arn
  ]
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr_repository.repository_url
}
