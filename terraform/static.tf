data "aws_acm_certificate" "wildcard" {
  domain      = "diegorocha.com.br"
  most_recent = true
}

resource "aws_s3_bucket" "diegorocha_com_br" {
  bucket = "diegorocha.com.br"
  acl    = "public-read"

  tags = {
    service = "diegorocha.com.br"
    backup  = "false"
  }
}

resource "aws_s3_bucket_cors_configuration" "diegorocha_com_br" {
  bucket = aws_s3_bucket.diegorocha_com_br.bucket

  cors_rule {
    allowed_headers = [
    "*"]
    allowed_methods = [
    "GET"]
    allowed_origins = [
      "https://diegorocha.com.br",
      "https://www.diegorocha.com.br",
      "https://diegosrocha.com.br",
      "https://diegorocha.dev",
      "http://localhost:8000",
    ]
    expose_headers = [
    "ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_website_configuration" "diegorocha_com_br" {
  bucket = aws_s3_bucket.diegorocha_com_br.bucket

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "not_found.html"
  }

}

resource "aws_s3_bucket_policy" "diegorocha_com_br_policy" {
  bucket = aws_s3_bucket.diegorocha_com_br.id

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
          "${aws_s3_bucket.diegorocha_com_br.arn}/*"
        ]
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

resource "aws_cloudfront_distribution" "diegorocha_com_br" {
  origin {
    domain_name = aws_s3_bucket.diegorocha_com_br.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.diegorocha_com_br.bucket
  }
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Distribution for diegorocha.com.br"
  default_root_object = "index.html"

  aliases = [
    "diegorocha.com.br",
    "www.diegorocha.com.br",
    "diegosrocha.com.br",
    "diegorocha.dev",
  ]

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
