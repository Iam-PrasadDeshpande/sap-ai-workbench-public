class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    data value type zr4_amount.
    rv = value.
  endmethod.
endclass.
