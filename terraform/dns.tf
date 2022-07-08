data "aws_route53_zone" "diegorocha_com_br" {
  name = "diegorocha.com.br"
}

data "aws_route53_zone" "diegosrocha_com_br" {
  name = "diegosrocha.com.br"
}

data "aws_route53_zone" "diegorocha_dev" {
  name = "diegorocha.dev"
}

locals {
  cloudfront_aliases_zone_ids = {
    "diegorocha.com.br"     = data.aws_route53_zone.diegorocha_com_br.zone_id
    "www.diegorocha.com.br" = data.aws_route53_zone.diegorocha_com_br.zone_id
    "diegosrocha.com.br"    = data.aws_route53_zone.diegosrocha_com_br.zone_id
    "diegorocha.dev"        = data.aws_route53_zone.diegorocha_dev.zone_id
  }
  cloudfront_aliases_record_types = [
    "A",
    "AAAA",
  ]
  cloudfront_aliases_records = flatten([
    for type in local.cloudfront_aliases_record_types : [
      for domain, zone_id in local.cloudfront_aliases_zone_ids : {
        domain  = domain
        zone_id = zone_id
        type    = type
      }
  ]])
}

resource "aws_route53_record" "cloudfront_aliases" {
  for_each = {
    for record in local.cloudfront_aliases_records : "${record.domain}_${record.type}" => record
  }
  zone_id = each.value.zone_id
  name    = each.value.domain
  type    = each.value.type

  alias {
    name                   = aws_cloudfront_distribution.diegorocha_com_br.domain_name
    zone_id                = aws_cloudfront_distribution.diegorocha_com_br.hosted_zone_id
    evaluate_target_health = false
  }
}
