#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <string.h>

#define COLUMNSIZE 19
#define NUMCOLUMNS 8
#define BYTESIZE 4
#define FREECELLS 0x01008AB0
#define FOUNDATIONS 0x01008AC0
LPVOID TABLEAU[8] = {(LPVOID)0x01008B04, (LPVOID)0x01008B58, (LPVOID)0x01008BAC, (LPVOID)0x01008C00, (LPVOID)0x01008C54, (LPVOID)0x01008CA8, (LPVOID)0x01008C5C, (LPVOID)0x01008D50};
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

int get_freecells(unsigned char* board) {

    char *processName = "freecell.exe";
    DWORD pid = find_pid(processName);
    if (pid == -1) {
        printf("Failed to find pid of process named %s\n", processName);
        return -1;
    }

    // Open process of the running executable
    HANDLE processHandle = OpenProcess(PROCESS_VM_READ, FALSE, pid);
    if (processHandle == NULL) {
        printf("Failed to open process. Error code: %ld\n", GetLastError());
        return -1;
    }

    // Read the tableau
    LPVOID addressToRead = (LPVOID)FREECELLS;
    SIZE_T bytesRead;
    BYTE buffer[4*BYTESIZE]; // Buffer to store the read data
    if (!ReadProcessMemory(processHandle, addressToRead, buffer, 4*BYTESIZE, &bytesRead)) {
        printf("Failed to read from process memory. Error code: %ld\n", GetLastError());
        CloseHandle(processHandle);
        return -1;
    }

    for (int i=0; i<4*BYTESIZE; i+=4) {
        board[i/BYTESIZE] = buffer[i];
    }

    CloseHandle(processHandle);

    return 0;

}

int get_foundations(unsigned char* board) {

    char *processName = "freecell.exe";
    DWORD pid = find_pid(processName);
    if (pid == -1) {
        printf("Failed to find pid of process named %s\n", processName);
        return -1;
    }

    // Open process of the running executable
    HANDLE processHandle = OpenProcess(PROCESS_VM_READ, FALSE, pid);
    if (processHandle == NULL) {
        printf("Failed to open process. Error code: %ld\n", GetLastError());
        return -1;
    }

    // Read the tableau
    LPVOID addressToRead = (LPVOID)FOUNDATIONS;
    SIZE_T bytesRead;
    BYTE buffer[4*BYTESIZE]; // Buffer to store the read data
    if (!ReadProcessMemory(processHandle, addressToRead, buffer, 4*BYTESIZE, &bytesRead)) {
        printf("Failed to read from process memory. Error code: %ld\n", GetLastError());
        CloseHandle(processHandle);
        return -1;
    }

    for (int i=0; i<4*BYTESIZE; i+=4) {
        board[i/BYTESIZE] = buffer[i];
    }

    CloseHandle(processHandle);

    return 0;

}

int get_tableau(unsigned char* board) {

    // board is an array of 8*19 = 152 unsigned chars
    // Initializing board to 0xff
    for (int i=0; i<COLUMNSIZE*NUMCOLUMNS; i++) {
        board[i] = 0xff;
    }

    char *processName = "freecell.exe";
    DWORD pid = find_pid(processName);
    if (pid == -1) {
        printf("Failed to find pid of process named %s\n", processName);
        return -1;
    }

    // Open process of the running executable
    HANDLE processHandle = OpenProcess(PROCESS_VM_READ, FALSE, pid);
    if (processHandle == NULL) {
        printf("Failed to open process. Error code: %ld\n", GetLastError());
        return -1;
    }

    for (int i=0; i<NUMCOLUMNS; i++) {
        LPVOID addressToRead = TABLEAU[i];
        SIZE_T bytesRead;
        BYTE buffer[BYTESIZE*COLUMNSIZE]; // Buffer to store the read data
        if (!ReadProcessMemory(processHandle, addressToRead, buffer, BYTESIZE*COLUMNSIZE, &bytesRead)) {
            printf("Failed to read from process memory. Error code: %ld\n", GetLastError());
            CloseHandle(processHandle);
            return -1;
        }
        for (int j=0; j<BYTESIZE*COLUMNSIZE; j+=4) {
            board[(COLUMNSIZE*i)+(j/BYTESIZE)] = buffer[j];
        }
    }

    CloseHandle(processHandle);

    return 0;

}