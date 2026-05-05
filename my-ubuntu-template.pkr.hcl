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
  default = "my-ubuntu-template"
}

variable "vm_id" { type = number, default = 9001 }
variable "vm_disk_size" { type = string, default = "40G" }
variable "iso_file" {
  type    = string
  default = "local:iso/ubuntu-24.04-live-server-amd64.iso"
}

source "proxmox-iso" "linux" {
  proxmox_url              = var.proxmox_url
  username                 = var.proxmox_username
  password                 = var.proxmox_password
  insecure_skip_tls_verify = var.proxmox_skip_tls_verify

  node                 = var.proxmox_host
  pool                 = var.proxmox_pool
  vm_id                = var.vm_id
  vm_name              = var.vm_name
  template_description = "Ubuntu template built for Ludus"

  cores           = 2
  memory          = 4096
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

  communicator = "ssh"
  ssh_username = "localuser"
  ssh_password = "password"
  ssh_timeout  = "45m"

  http_directory = "http"
}

build {
  name    = "ubuntu-template-build"
  sources = ["source.proxmox-iso.linux"]

  provisioner "shell" {
    script = "scripts/linux-bootstrap.sh"
  }

  provisioner "shell" {
    script = "scripts/cleanup.sh"
  }
}
