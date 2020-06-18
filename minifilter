/*++

Module Name:

    FsFilter1.c

Abstract:

    This is the main module of the FsFilter1 miniFilter driver.

Environment:

    Kernel mode

--*/

#include <fltKernel.h>
#include <dontuse.h>

PFLT_FILTER FilterHandle = NULL;

const FLT_OPERATION_REGISTRATION Callbacks[] = {
    {IRP_MJ_CREATE,0,MiniPreCreate,MiniPostCreate},
    {IRP_MJ_WRITE,0,MiniPreWrite,NULL},
    {IRP_MJ_OPERATION_END}
};


const FLT_REGISTRATION FilterRegistration = {
    sizeof(FLT_REGISTRATION),
    FLT_REGISTRATION_VERSION,
    0,
    NULL,
    Callbacks,
    MiniUnload,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
};

NTSTATUS MiniUnload(FLT_FILTER_UNLOAD_FLAGS Flags) {

    KdPrint(("driver unload \r\n"));
    FltUnregisterFilter(FilterHandle);

    return STATUS_SUCCESS;

}

NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {

    NTSTATUS status;

    status = FltRegisterFilter(DriverObject, &FilterRegistration, &FilterHandle);

    /*Check status of Function */
    if (NT_SUCCESS(status)) {

        status = FltStartFiltering(FilterHandle);

        /*Check status of Function */
        if (!NT_SUCCESS(status)) {

            /* Unregister filter if status = failed*/
            FltUnregisterFilter(FilterHandle);

        }

    }

    return status;

}
