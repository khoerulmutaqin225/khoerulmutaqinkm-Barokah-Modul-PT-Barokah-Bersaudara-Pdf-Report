<!-- # barokah_module
<!-- Untuk membuat debug di odoo -->
1. Matikan server di service
2. download arkademy
3. buka odoo13/server
4. create config
5. ketik odoo
6.  paste dengan file ini 
7. Matikan advision anti virus
// -- ------------------------------------
// -- Perhatian
// -- Khusus untuk Windows User : 
// -- hasil dari Copy Path harus diganti dengan double-backslash \\
// -- ------------------------------------
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Odoo",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "console": "integratedTerminal",
            "python": "C:\\Program Files\\Odoo 13.0\\python\\python.exe",
            "program": "C:\\Program Files\\Odoo 13.0\\server\\odoo-bin",
            "args": [
                "--config=C:\\Program Files\\Odoo 13.0\\server\\odoo.conf",
                // "--database=tutor1,tutor2",
                // "--update=nama_folder1,nama_folder2"
            ]
        }
    ]
} -->
