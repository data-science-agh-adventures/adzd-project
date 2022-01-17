# Projekt z ADZD

Introduction to Azure Cosmos DB

## Jak korzystać z "symulacji urządzeń IoT"

Jest skrypt `.ps1` - `run-iot-simulation.ps1`, który odpowiada za wszystkie przygotowywania i ustawienia (tworzenie konta Cosmos DB, tworzenie bazy danych na tym koncie, tworzenie kontenera w tej bazie). Oprócz tego on uruchamia $n$ instancji skryptu `cosmosdb_iot_simulator.py`, które co jakiś czas wysyłają przykładowe dane z "urządzenia IoT" na serwer.

> Przed uruchomieniem `.ps1` skryptu trzeba upewnić się, że sesja powershell jest zalogowana:

```powershell
$ az login
```

Ogólny zapis skryptu:

```powershell
$ powershell.exe -ExecutionPolicy Bypass -File .\run-iot-simulation.ps1 --dbName "<database_name>" --containerName "<container_name>" --resourceGroup "<resource_group>" --accountName "<account_name>" --nTestsToRun <integer>
```

Parametry:
- `dbName` - nazwa bazy danych, może i nie istnieć, Cosmos ją stworzy;
- `containerName` - nazwa kontenera w danej bazie, też może nie istnieć;
- `resourceGroup` - nazwa grupy zasobów Azure, na pewno musi istnieć i zalogowany użytkownik musi mieć do niej uprawnienia;
- `accountName` - nazwa konta Cosmos DB, też może nie istnieć;
- `nTestsToRun` - liczba instancji skryptu `cosmosdb_iot_simulator.py` jednocześnie uruchomionych.

---

> Mały hint (nie ma nic wspólnego z projektem). Żeby używać w git powershell'a ssh konfig, który leży w WSL, to można zrobić tak:

```powershell
$ git config --local core.sshCommand 'ssh -i \\\\wsl$\\Ubuntu-20.04\\home\\<user>\\.ssh\\<target_private_key> -F \\\\wsl$\\Ubuntu-20.04\\home\\<user>\\.ssh\\config -o IdentitiesOnly=yes'
```

> potem można spokojnie już dawać `git push`, `git pull` itd.
