terraform {
  required_version = "1.4.5"
  required_providers { aws = { version = "5.1.0" } }
  backend "s3" {
    bucket               = "diegor-terraform"
    workspace_key_prefix = ""
    key                  = "diegorocha.com.br/terraform.tfstate"
    region               = "us-east-1"
    profile              = "diego"
  }
}

provider "google" {
  project = "diegor-infra"
  region  = "us-central1"
}

provider "google-beta" {
  project = "diegor-infra"
  region  = "us-central1"
}
