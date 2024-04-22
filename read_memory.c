// Currently, this code looks for a running freecell game and prints the bytes that correspond to the top-left card.

#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <string.h>

#define streq(a, b) (strcmp(a, b) == 0)

DWORD find_pid(char *processName) {

    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        printf("Failed to create process snapshot. Error code: %lu\n", GetLastError());
        return -1;
    }

    PROCESSENTRY32 entry;
    entry.dwSize = sizeof(entry);

    // Get the first process
    if (!Process32First(snapshot, &entry)) {
        printf("Failed to retrieve process information. Error code: %lu\n", GetLastError());
        CloseHandle(snapshot);
        return -1;
    }

    // Iterate through processes and print their PIDs
    int pid = -1;
    do {
        if (streq(entry.szExeFile, processName)) {
            pid = entry.th32ProcessID;
            break;
        }
    } while (Process32Next(snapshot, &entry));

    CloseHandle(snapshot);
    return (DWORD)pid;
}

int main(int argc, char *argv[]) {

    char *processName = "freecell.exe";
    DWORD pid = find_pid(processName);

    // Open process of the running executable
    HANDLE processHandle = OpenProcess(PROCESS_VM_READ, FALSE, pid);
    if (processHandle == NULL) {
        printf("Failed to open process. Error code: %d\n", GetLastError());
        return 1;
    }
    
    // Read the virtual memory of the process
    LPVOID addressToRead = (LPVOID)0x01008B58;
    SIZE_T bytesRead;
    // BYTE buffer[SIZE]; // Buffer to store the read data
    BYTE buffer[4]; // Buffer to store the read data
    if (!ReadProcessMemory(processHandle, addressToRead, buffer, 4, &bytesRead)) {
        printf("Failed to read from process memory. Error code: %d\n", GetLastError());
        CloseHandle(processHandle);
        return 1;
    }
    printf("Read memory!\n");
    printf("%02x\n", buffer[0]);
    printf("%02x\n", buffer[1]);
    printf("%02x\n", buffer[2]);
    printf("%02x\n", buffer[3]);

    CloseHandle(processHandle);

    return 0;
}
