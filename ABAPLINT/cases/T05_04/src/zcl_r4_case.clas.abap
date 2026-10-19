class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    call function 'ZR4_UPDATE_MISSING' in update task.
    commit work and wait.
    rv = sy-subrc.
  endmethod.
endclass.
