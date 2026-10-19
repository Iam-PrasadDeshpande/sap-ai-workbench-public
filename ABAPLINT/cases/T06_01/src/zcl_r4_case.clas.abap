class zcl_r4_case definition public final create public.
  public section.
    methods run importing numerator type i denominator type i returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    rv = trunc( numerator / denominator ).
  endmethod.
endclass.
