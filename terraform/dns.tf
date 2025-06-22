locals {
  alias_zones = {
    for domain in local.cloudfront_aliases :
    domain => data.terraform_remote_state.infra.outputs.dns[replace(domain, "www.", "")].id
  }
}

resource "aws_route53_record" "alias" {
  for_each = local.alias_zones

  zone_id = each.value
  name    = each.key
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.diegorocha_com_br.domain_name
    zone_id                = aws_cloudfront_distribution.diegorocha_com_br.hosted_zone_id
    evaluate_target_health = false
  }
}
