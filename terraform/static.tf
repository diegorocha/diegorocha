data "aws_caller_identity" "current" {}

data "aws_acm_certificate" "wildcard" {
  domain      = "diegorocha.com.br"
  most_recent = true
}

locals {
  cloudfront_aliases = concat(keys(local.domains_zones), keys(local.subdomains_zones))
}

resource "aws_s3_bucket" "diegorocha_com_br" {
  bucket = "diegorocha.com.br"

  tags = {
    service = "diegorocha.com.br"
    backup  = "false"
  }
}

resource "aws_s3_bucket_ownership_controls" "diegorocha_com_br" {
  bucket = aws_s3_bucket.diegorocha_com_br.bucket
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "diegorocha_com_br" {
  bucket = aws_s3_bucket.diegorocha_com_br.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "diegorocha_com_br_policy" {
  bucket = aws_s3_bucket.diegorocha_com_br.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowAllToRootAndCreator",
        Effect = "Allow",
        Principal = {
          "AWS" : [
            "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
            data.aws_caller_identity.current.arn,
          ]
        }
        Action = "s3:*",
        Resource = [
          aws_s3_bucket.diegorocha_com_br.arn,
          "${aws_s3_bucket.diegorocha_com_br.arn}/*",
        ]
      },
      {
        Sid    = "AllowCloudFrontServicePrincipalReadOnly",
        Effect = "Allow",
        Principal = {
          Service = "cloudfront.amazonaws.com"
        },
        Action   = "s3:GetObject",
        Resource = "${aws_s3_bucket.diegorocha_com_br.arn}/*",
        Condition = {
          "StringEquals" : {
            "AWS:SourceArn" : aws_cloudfront_distribution.diegorocha_com_br.arn,
          }
        }
      },
    ]
  })
}

resource "aws_iam_policy" "policy_diegorocha_com_br" {
  name        = "policy_diegorocha_com_br"
  path        = "/"
  description = "Policy to allow read/write to ${aws_s3_bucket.diegorocha_com_br.bucket} bucket"

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
          aws_s3_bucket.diegorocha_com_br.arn,
          "${aws_s3_bucket.diegorocha_com_br.arn}/*"
        ]
      },

    ]
  })
}

resource "aws_cloudfront_origin_access_control" "diegorocha_com_br" {
  name                              = aws_s3_bucket.diegorocha_com_br.bucket
  description                       = "${aws_s3_bucket.diegorocha_com_br.bucket} Policy"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "diegorocha_com_br" {
  origin {
    origin_access_control_id = aws_cloudfront_origin_access_control.diegorocha_com_br.id
    domain_name              = aws_s3_bucket.diegorocha_com_br.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.diegorocha_com_br.bucket
  }
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Distribution for diegorocha.com.br"
  default_root_object = "index.html"

  custom_error_response {
    error_code         = 403
    response_code      = 404
    response_page_path = "/not_found.html"
  }

  custom_error_response {
    error_code         = 404
    response_code      = 404
    response_page_path = "/not_found.html"
  }

  aliases = local.cloudfront_aliases

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.diegorocha_com_br.bucket

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    min_ttl                = 0
    default_ttl            = 300
    max_ttl                = 600
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.wildcard.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }

  tags = {
    service = "diegorocha.com.br"
    backup  = "false"
  }
}
