class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    data header type zr4_header.
    rv = header-amount.
  endmethod.
endclass.
