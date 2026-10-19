class zcl_r4_case definition public final create public.
  public section.
    methods run importing iv type i returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    rv = zcl_r4_dep=>inc( iv ).
  endmethod.
endclass.
