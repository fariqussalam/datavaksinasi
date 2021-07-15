(function ($) {
    "use strict";

    // Add active state to sidbar nav links
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
            ],
            "columnDefs": [
                {
                    "targets": 6,
                    "data": "hadir",
                    "render": function (data, type, row, meta) {
                        var template = '<div>' +
                            '<button type="button" data-nik="' + row.nik + '" data-nama="' + row.nama_lengkap + '" data-url="/backend/registrasi-kehadiran/' + parseInt(row.id) + '" class="btn btn-sm btn-primary js-tandai-kehadiran">Tandai Kehadiran</button>' +
                            '</div>'
                        if (row.hadir == true) {
                            return "-"
                        } else {
                            return template;
                        }
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

})(jQuery);
