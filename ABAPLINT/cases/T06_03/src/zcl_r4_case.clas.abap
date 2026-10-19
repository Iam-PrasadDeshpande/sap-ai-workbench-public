class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    data amount type p length 8 decimals 2.
    amount = conv decfloat34( '1.235' ).
    rv = amount * 100.
  endmethod.
endclass.
