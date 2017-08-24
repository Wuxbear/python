
FGT-80C-manager = {
        "register":[
            "80C RELOGIN",
### vap register
            "console_write config wireless-controller vap\n",
            "console_write edit FAP_VAP_%DN%_1\n",
            "console_write set ssid %SN%_%DN%_1\n",
            "console_write end\n",
            "console_write show wireless-controller vap FAP_VAP_%DN%_1\n",
            "console_write config wireless-controller vap\n",
            "console_write edit FAP_VAP_%DN%_2\n",
            "console_write set ssid %SN%_%DN%_2\n",
            "console_write end\n",
            "console_write show wireless-controller vap FAP_VAP_%DN%_2\n",
### wtp register
            "console_write config wireless-controller wtp\n",
            "console_write edit %SN%\n",
            "console_write set admin enable\n",
            "console_write set login-enable enable\n",
            "console_write set wtp-profile %MODEL%_Profile_%DN%\n",
            "console_write next\n",
            "console_write end\n",
            "console_write show wireless-controller wtp $10\n",
### check & return IP
            "consolesend get wireless-controller wtp-status %SN%\n"
            "consolewaitrge 10 wtp-id\s*:\s*%SN%"
            "consolereadrge $17 10 local-ipv4-addr\s*:\s*(192\.168\.1\.\d+)"
            "consolewaitrge 10 connection-state\s*:\s*Connected"
            ###"message [$18] is sent at [$D $T]."

            ],
        "remove":[
            "80C RELOGIN",
            "console_write conf wireless-controller wtp\n",
            "console_write delete %SN%\n",
            "console_write end\n",
            "console_write show wireless-controller wtp %SN%\n",
            "console_read 10 entry is not found in table",
            ###"return remove message"
            ],
}

