class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    select sum( amount ) from zr4_data where id > 99 into @rv.
  endmethod.
endclass.
