// stupid little extension to add base-10 logarithm and 10^x to sqlite
#define _GNU_SOURCE
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
#include <assert.h>
#include <stdlib.h>
#include <math.h>

static void log10func(sqlite3_context *context, int argc, sqlite3_value **argv) {
	assert(argc == 1);
	double x = sqlite3_value_double(argv[0]);
	if (x > 0)
		sqlite3_result_double(context, log10(x));
	else
		sqlite3_result_error(context, "logarithm of negative number", 28);
}

static void exp10func(sqlite3_context *context, int argc, sqlite3_value **argv) {
	assert(argc == 1);
	double x = sqlite3_value_double(argv[0]);
	sqlite3_result_double(context, exp10(x));
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int sqlite3_extension_init(sqlite3 *db, char **err, const sqlite3_api_routines *api) {
	(void) err;
	SQLITE_EXTENSION_INIT2(api);
	int rc = sqlite3_create_function(db, "log10", 1, SQLITE_UTF8, NULL, log10func, NULL, NULL);
	if (rc == SQLITE_OK)
		rc = sqlite3_create_function(db, "exp10", 1, SQLITE_UTF8, NULL, exp10func, NULL, NULL);
	return rc;
}
