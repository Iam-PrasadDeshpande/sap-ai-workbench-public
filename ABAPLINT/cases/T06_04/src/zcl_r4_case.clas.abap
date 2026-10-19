class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    data amount type decfloat34.
    amount = conv decfloat34( '9007199254740993' ) - conv decfloat34( '9007199254740992' ).
    rv = amount.
  endmethod.
endclass.
