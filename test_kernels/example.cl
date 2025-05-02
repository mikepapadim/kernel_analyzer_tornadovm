#pragma OPENCL EXTENSION cl_khr_fp64 : enable  
#pragma OPENCL EXTENSION cl_khr_fp16 : enable  
#pragma OPENCL EXTENSION cl_khr_int64_base_atomics : enable  
__kernel void matmulUnroll4WithResidual(__global long *_kernel_context, __constant uchar *_constant_region, __local uchar *_local_region, __global int *_atomics, __global uchar *xout, __global uchar *x, __global uchar *w, __private int n, __private int d, __global uchar *positionAndLayer)
{
  float f_38, f_70, f_33, f_65, f_24, f_56, f_55, f_54, f_19, f_83, f_82, f_49, f_13, f_76, f_75, f_74, f_73, f_40, f_72, f_39, f_71; 
  int i_57, i_59, i_60, i_61, i_66, i_5, i_6, i_7, i_8, i_9, i_10, i_11, i_12, i_77, i_14, i_78, i_15, i_20, i_84, i_25, i_27, i_28, i_29, i_34, i_41, i_43, i_44, i_45, i_50; 
  bool b_26, b_42, b_58; 
  long l_30, l_62, l_31, l_63, l_51, l_52, l_21, l_22, l_46, l_47, l_79, l_16, l_80, l_17, l_35, l_67, l_36, l_68; 
  ulong ul_3, ul_2, ul_1, ul_0, ul_32, ul_64, ul_37, ul_69, ul_4, ul_18, ul_81, ul_48, ul_23, ul_53; 

  // BLOCK 0
  ul_0  =  (ulong) xout;
  ul_1  =  (ulong) x;
  ul_2  =  (ulong) w;
  ul_3  =  (ulong) positionAndLayer;
  ul_4  =  ul_3 + 28L;
  i_5  =  *((__global int *) ul_4);
  i_6  =  i_5 << 24;
  i_7  =  i_6 + 6;
  i_8  =  get_global_size(0);
  i_9  =  get_global_id(0);
  // BLOCK 1 MERGES [0 14 ]
  i_10  =  i_9;
  for(;i_10 < 2048;)
  {
    // BLOCK 2
    i_11  =  i_10 << 13;
    i_12  =  i_11 + i_7;
    // BLOCK 3 MERGES [2 13 ]
    f_13  =  0.0F;
    i_14  =  0;
    for(;i_14 < 8192;)
    {
      // BLOCK 4
      i_15  =  i_12 + i_14;
      l_16  =  (long) i_15;
      l_17  =  l_16 << 2;
      ul_18  =  ul_2 + l_17;
      f_19  =  *((__global float *) ul_18);
      i_20  =  i_14 + 6;
      l_21  =  (long) i_20;
      l_22  =  l_21 << 2;
      ul_23  =  ul_1 + l_22;
      f_24  =  *((__global float *) ul_23);
      i_25  =  i_14 + 1;
      b_26  =  i_25 < 8192;
      if(b_26)
      {
        // BLOCK 5
        i_27  =  i_6 + 7;
        i_28  =  i_27 + i_11;
        i_29  =  i_28 + i_14;
        l_30  =  (long) i_29;
        l_31  =  l_30 << 2;
        ul_32  =  ul_2 + l_31;
        f_33  =  *((__global float *) ul_32);
        i_34  =  i_14 + 7;
        l_35  =  (long) i_34;
        l_36  =  l_35 << 2;
        ul_37  =  ul_1 + l_36;
        f_38  =  *((__global float *) ul_37);
        f_39  =  f_33 * f_38;
        f_40  =  f_39;
      }  // B5
      else
      {
        // BLOCK 6
        f_40  =  0.0F;
      }  // B6
      // BLOCK 7 MERGES [5 6 ]
      i_41  =  i_14 + 2;
      b_42  =  i_41 < 8192;
      if(b_42)
      {
        // BLOCK 8
        i_43  =  i_6 + 8;
        i_44  =  i_43 + i_11;
        i_45  =  i_44 + i_14;
        l_46  =  (long) i_45;
        l_47  =  l_46 << 2;
        ul_48  =  ul_2 + l_47;
        f_49  =  *((__global float *) ul_48);
        i_50  =  i_14 + 8;
        l_51  =  (long) i_50;
        l_52  =  l_51 << 2;
        ul_53  =  ul_1 + l_52;
        f_54  =  *((__global float *) ul_53);
        f_55  =  f_49 * f_54;
        f_56  =  f_55;
      }  // B8
      else
      {
        // BLOCK 9
        f_56  =  0.0F;
      }  // B9
      // BLOCK 10 MERGES [8 9 ]
      i_57  =  i_14 + 3;
      b_58  =  i_57 < 8192;
      if(b_58)
      {
        // BLOCK 11
        i_59  =  i_6 + 9;
        i_60  =  i_59 + i_11;
        i_61  =  i_60 + i_14;
        l_62  =  (long) i_61;
        l_63  =  l_62 << 2;
        ul_64  =  ul_2 + l_63;
        f_65  =  *((__global float *) ul_64);
        i_66  =  i_14 + 9;
        l_67  =  (long) i_66;
        l_68  =  l_67 << 2;
        ul_69  =  ul_1 + l_68;
        f_70  =  *((__global float *) ul_69);
        f_71  =  f_65 * f_70;
        f_72  =  f_71;
      }  // B11
      else
      {
        // BLOCK 12
        f_72  =  0.0F;
      }  // B12
      // BLOCK 13 MERGES [11 12 ]
      f_73  =  fma(f_19, f_24, f_40);
      f_74  =  f_56 + f_73;
      f_75  =  f_72 + f_74;
      f_76  =  f_13 + f_75;
      i_77  =  i_14 + 4;
      f_13  =  f_76;
      i_14  =  i_77;
    }  // B13
    // BLOCK 14
    i_78  =  i_10 + 6;
    l_79  =  (long) i_78;
    l_80  =  l_79 << 2;
    ul_81  =  ul_0 + l_80;
    f_82  =  *((__global float *) ul_81);
    f_83  =  f_82 + f_13;
    *((__global float *) ul_81)  =  f_83;
    i_84  =  i_8 + i_10;
    i_10  =  i_84;
  }  // B14
  // BLOCK 15
  return;
}  //  kernel

