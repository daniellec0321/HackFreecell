// MathLibrary.h - Contains declarations of math functions
#pragma once

#ifdef LIB_EXPORTS
#define LIB_API __declspec(dllexport)
#else
#define LIB_API __declspec(dllimport)
#endif

LIB_API int test_func(char *erm);