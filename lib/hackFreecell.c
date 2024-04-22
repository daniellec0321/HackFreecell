// Currently, this code looks for a running freecell game and prints the bytes that correspond to the top-left card.

#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <string.h>

#define COLUMN1 0x01008B04
#define COLUMN2 0x01008B58
#define COLUMN3 0x01008BAC
#define COLUMN4 0x01008C00
#define COLUMN5 0x01008C54
#define COLUMN6 0x01008CA8
#define COLUMN7 0x01008C5C
#define COLUMN8 0x01008D50
#define TABLEAU 0x01008AB0
#define STACK 0x01008AC0

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

int get_tableau(unsigned short* board) {

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

    CloseHandle(processHandle);

    return 0;

}

int thing(void) {

    char *processName = "freecell.exe";
    DWORD pid = find_pid(processName);
    if (pid == -1) {
        printf("Failed to find pid of process named %s\n", processName);
        return 1;
    }

    // Open process of the running executable
    HANDLE processHandle = OpenProcess(PROCESS_VM_READ, FALSE, pid);
    if (processHandle == NULL) {
        printf("Failed to open process. Error code: %ld\n", GetLastError());
        return 1;
    }
    
    // Read the virtual memory of the process
    LPVOID addressToRead = (LPVOID)0x01008B04;
    SIZE_T bytesRead;
    BYTE buffer[4]; // Buffer to store the read data
    if (!ReadProcessMemory(processHandle, addressToRead, buffer, 4, &bytesRead)) {
        printf("Failed to read from process memory. Error code: %ld\n", GetLastError());
        CloseHandle(processHandle);
        return 1;
    }
    if (buffer[0] == 0xff) {
        printf("No card data yet. Make sure to begin a game before running the program.\n");
    } else {
        printf("Top left card is %02x\n", buffer[0]);
    }

    CloseHandle(processHandle);

    return 0;
}

// unsigned short* test(void) {
//     board = malloc(8*sizeof(unsigned short));
//     for (int i=0; i<8; i++) {
//         board[i] = 0xff;
//     }
//     return board;
// }

// void clean_board(void) {
//     if (board) free(board);
// }