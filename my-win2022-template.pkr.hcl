packer {
  required_plugins {
    proxmox = {
      source  = "github.com/hashicorp/proxmox"
      version = ">= 1.1.0"
    }
  }
}

# Required Ludus variables
variable "proxmox_url" { type = string }
variable "proxmox_host" { type = string }
variable "proxmox_username" { type = string }
variable "proxmox_password" {
  type      = string
  sensitive = true
}
variable "proxmox_storage_pool" { type = string }
variable "proxmox_storage_format" { type = string }
variable "proxmox_skip_tls_verify" { type = bool }
variable "proxmox_pool" { type = string }
variable "iso_storage_pool" { type = string }
variable "ansible_home" { type = string }
variable "ludus_nat_interface" { type = string }

variable "vm_name" {
  type    = string
  default = "my-win2022-template"
}

variable "vm_id" { type = number, default = 9101 }
variable "vm_disk_size" { type = string, default = "64G" }
variable "iso_file" {
  type    = string
  default = "local:iso/Win_Server_2022.iso"
}

source "proxmox-iso" "windows" {
  proxmox_url              = var.proxmox_url
  username                 = var.proxmox_username
  password                 = var.proxmox_password
  insecure_skip_tls_verify = var.proxmox_skip_tls_verify

  node                 = var.proxmox_host
  pool                 = var.proxmox_pool
  vm_id                = var.vm_id
  vm_name              = var.vm_name
  template_description = "Windows Server 2022 template built for Ludus"

  cores           = 4
  memory          = 8192
  cpu_type        = "host"
  qemu_agent      = true
  scsi_controller = "virtio-scsi-single"

  disks {
    disk_size    = var.vm_disk_size
    format       = var.proxmox_storage_format
    storage_pool = var.proxmox_storage_pool
    type         = "virtio"
    discard      = true
    io_thread    = true
  }

  network_adapters {
    bridge = var.ludus_nat_interface
    model  = "virtio"
  }

  iso_file         = var.iso_file
  iso_storage_pool = var.iso_storage_pool
  unmount_iso      = true

  communicator   = "winrm"
  winrm_username = "localuser"
  winrm_password = "password"
  winrm_use_ssl  = true
  winrm_insecure = true
  winrm_timeout  = "2h"

  http_directory = "http"
}

build {
  name    = "win2022-template-build"
  sources = ["source.proxmox-iso.windows"]

  provisioner "powershell" {
    script = "scripts/windows-bootstrap.ps1"
  }
}
