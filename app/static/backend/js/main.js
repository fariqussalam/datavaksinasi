(function ($) {
    "use strict";

    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function (e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });

    $(document).ready(function () {

        $('.js-tabel-daftar-peserta').DataTable({
            "ajax": '/backend/api/daftar-peserta',
            "order": [[4, "asc"]],
            "lengthChange": false,
            "pageLength": 15,
            "columns": [
                {"data": "nama_lengkap"},
                {"data": "nik"},
                {"data": "alamat_ktp"},
                {"data": "no_hp"},
                {"data": "batch"},
                // { "data": "hari_vaksin" },
                {"data": "peserta_hadir"},
                {"data": "sudah_vaksin"},
                {"data": "penyelenggara"},
            ],
            "columnDefs": [
                  {
                    "targets": 8,
                    "data": "sudah_vaksin",
                    "render": function (data, type, row, meta) {
                        var template = '<div>'
                        if (row.hadir != true) {
                            template += '<button type="button" data-nik="' + row.nik + '" data-nama="' + row.nama_lengkap + '" data-url="/backend/registrasi-kehadiran/' + parseInt(row.id) + '" class="btn btn-sm btn-primary js-tandai-kehadiran m-1">Tandai Kehadiran</button>'
                        }
                        if (row.is_sudah_vaksin != true) {
                            template += '<button type="button" data-nik="' + row.nik + '" data-nama="' + row.nama_lengkap + '" data-url="/backend/registrasi-sudah-vaksin/' + parseInt(row.id) + '" class="btn btn-sm btn-success js-tandai-sudah-vaksin m-1">Tandai Sudah Vaksin</button>'
                        }
                        template += "</div>"
                        return template;

                    }
                },
                {
                    "targets": 9,
                    "data": "hadir",
                    "render": function (data, type, row, meta) {
                         var template_hadir = '<div>' +
                            ' <a href="/backend/registrasi/edit/' + parseInt(row.id) + '" class="btn btn-sm btn-info m-1">Edit</a>' +
                            ' <button data-nik="' + row.nik + '" data-nama="' + row.nama_lengkap + '" data-url="/backend/registrasi/hapus/' + parseInt(row.id) + '" class="btn btn-sm btn-danger m-1 js-hapus-peserta">Hapus</button>' +
                            '</div>'
                        return template_hadir
                    }
                }
            ]
        })

        $('.js-tabel-daftar-peserta-unit').DataTable({
            "ajax": '/backend/api/daftar-peserta',
            "order": [[4, "asc"]],
            "lengthChange": false,
            "pageLength": 15,
            "columns": [
                {"data": "nama_lengkap"},
                {"data": "nik"},
                {"data": "alamat_ktp"},
                {"data": "no_hp"},
                {"data": "batch"},
                // { "data": "hari_vaksin" },
                {"data": "peserta_hadir"},
                {"data": "sudah_vaksin"},
            ]
        })
    });

    $(document).on('click', '.js-tandai-kehadiran', function () {
        var nama = $(this).data("nama")
        var nik = $(this).data("nik")
        var url = $(this).data("url")
        $.confirm({
            title: 'Konfirmasi',
            content: 'Yakin Ingin Menandai Kehadiran ' + nama + " (NIK : " + nik + ") ?",
            buttons: {
                confirm: function () {
                    window.location.href = url
                },
                cancel: function () {}
            }
        });
    })

    $(document).on('click', '.js-tandai-sudah-vaksin', function () {
        var nama = $(this).data("nama")
        var nik = $(this).data("nik")
        var url = $(this).data("url")
        $.confirm({
            title: 'Konfirmasi',
            content: 'Yakin Ingin Menandai Vaksinasi ' + nama + " (NIK : " + nik + ") ?",
            buttons: {
                confirm: function () {
                    window.location.href = url
                },
                cancel: function () {}
            }
        });
    })

      $(document).on('click', '.js-hapus-peserta', function () {
        var nama = $(this).data("nama")
        var nik = $(this).data("nik")
        var url = $(this).data("url")
        $.confirm({
            title: 'Konfirmasi',
            content: 'Yakin Ingin Menghapus Data Peserta ' + nama + " (NIK : " + nik + ") ?",
            buttons: {
                confirm: function () {
                    window.location.href = url
                },
                cancel: function () {}
            }
        });
    })

})(jQuery);
