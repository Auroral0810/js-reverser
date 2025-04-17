#include <stdio.h>
#include <stdlib.h>
#include "match20.c"

extern void init_wasm(void);
extern char* get_sign(char*);

void init_wasm(){
    init_func_types();
    init_globals();
    init_memory();
    init_table();
    init_exports();
}

char* get_sign(char* content){
    u32 retptr = w2c___wbindgen_add_to_stack_pointer(-16);
    int content_len = (int)strlen(content);
    u32 content_ptr = w2c___wbindgen_malloc( content_len + 1);
    memcpy(w2c_memory.data + content_ptr, content, content_len + 1);
    w2c_sign(retptr, content_ptr, content_len);
    int out_ptr = 0;
    out_ptr += (w2c_memory.data + retptr)[0];
    out_ptr += (w2c_memory.data + retptr)[1] << 8;
    out_ptr += (w2c_memory.data + retptr)[2] << 16;
    out_ptr += (w2c_memory.data + retptr)[3] << 24;

    char* out_str = (char *)malloc(33);
    out_str[32] = 0;
    memcpy(out_str, w2c_memory.data + out_ptr, 32);
    return out_str;
}

int main(int argc,char *argv[]) {
    init_wasm();
    char* content = argv[1];

    u32 retptr = w2c___wbindgen_add_to_stack_pointer(-16);
    int content_len = (int)strlen(content);
    u32 content_ptr = w2c___wbindgen_malloc( content_len + 1);
    memcpy(w2c_memory.data + content_ptr, content, content_len + 1);
    w2c_sign(retptr, content_ptr, content_len);
    int out_ptr = 0;
    out_ptr += (w2c_memory.data + retptr)[0];
    out_ptr += (w2c_memory.data + retptr)[1] << 8;
    out_ptr += (w2c_memory.data + retptr)[2] << 16;
    out_ptr += (w2c_memory.data + retptr)[3] << 24;

    char* out_str = (char *)malloc(33);
    out_str[32] = 0;
    memcpy(out_str, w2c_memory.data + out_ptr, 32);
    printf("%s\n", out_str);

    free(out_str);

    return 0;
}