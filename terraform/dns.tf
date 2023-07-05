locals {
  domains_zones = {
    "diegorocha.com.br" = "diegorocha-com-br"
    "diegosrocha.com.br" = "diegosrocha-com-br"
    "diegorocha.dev" = "diegorocha-dev"
  }
  subdomains_zones = {
    "www.diegorocha.com.br" = "diegorocha-com-br"
  }
}

resource "google_dns_record_set" "alias" {
  for_each = local.domains_zones

  name = "${each.key}."
  type = "ALIAS"
  ttl  = 300

  managed_zone = each.value

  rrdatas = ["${aws_cloudfront_distribution.diegorocha_com_br.domain_name}."]
}

resource "google_dns_record_set" "cname" {
  for_each = local.subdomains_zones

  name = "${each.key}."
  type = "CNAME"
  ttl  = 300

  managed_zone = each.value

  rrdatas = ["${aws_cloudfront_distribution.diegorocha_com_br.domain_name}."]
}
