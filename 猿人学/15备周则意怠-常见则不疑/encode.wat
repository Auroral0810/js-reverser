(module
  (memory (export "memory") 4)
  (global $global0 (mut i32) (i32.const 66560))
  
  (func $encode (export "encode") (param $var0 i32) (param $var1 i32) (result i32)
    (local $var2 i32) (local $var3 i32) (local $var4 i32) (local $var5 i32)
    (local $var6 i32) (local $var7 i32) (local $var8 i32) (local $var9 i32)
    (local $var10 i32) (local $var11 i32) (local $var12 i32) (local $var13 i32)
    (local $var14 i32) (local $var15 i32) (local $var16 i32) (local $var17 i32)
    (local $var18 i32) (local $var19 i32) (local $var20 i32) (local $var21 i32)
    (local $var22 i32) (local $var23 i32) (local $var24 i32) (local $var25 i32)
    (local $var26 i32) (local $var27 i32) (local $var28 i32) (local $var29 i32)
    (local $var30 i32) (local $var31 i32) (local $var32 i32) (local $var33 i32)
    (local $var34 i32) (local $var35 i32) (local $var36 i32) (local $var37 i32)
    (local $var38 i32) (local $var39 i32) (local $var40 i32) (local $var41 i32)
    (local $var42 i32) (local $var43 i32) (local $var44 i32) (local $var45 i32)
    (local $var46 i32) (local $var47 i32) (local $var48 i32) (local $var49 i32)
    (local $var50 i32) (local $var51 i32) (local $var52 i32) (local $var53 i32)
    (local $var54 i32) (local $var55 i32) (local $var56 i32) (local $var57 i32)
    (local $var58 i32) (local $var59 i32) (local $var60 i32) (local $var61 i32)
    (local $var62 i32) (local $var63 i32) (local $var64 i32) (local $var65 i32)
    (local $var66 i32) (local $var67 i32) (local $var68 i32) (local $var69 i32)
    (local $var70 i32) (local $var71 i32) (local $var72 i32) (local $var73 i32)
    (local $var74 i32) (local $var75 i32) (local $var76 i32) (local $var77 i32)
    (local $var78 i32) (local $var79 i32) (local $var80 i32) (local $var81 i32)
    (local $var82 i32) (local $var83 i32) (local $var84 i32) (local $var85 i32)
    (local $var86 i32) (local $var87 i32) (local $var88 i32) (local $var89 i32)
    (local $var90 i32) (local $var91 i32) (local $var92 i32) (local $var93 i32)
    (local $var94 i32) (local $var95 i32) (local $var96 i32) (local $var97 i32)
    (local $var98 i32) (local $var99 i32) (local $var100 i32) (local $var101 i32)
    (local $var102 i32) (local $var103 i32) (local $var104 i32) (local $var105 i32)
    (local $var106 i32) (local $var107 i32) (local $var108 i32) (local $var109 i32)
    (local $var110 i32) (local $var111 i32) (local $var112 i32) (local $var113 i32)
    (local $var114 i32) (local $var115 i32) (local $var116 i32) (local $var117 i32)
    (local $var118 i32) (local $var119 i32) (local $var120 i32) (local $var121 i32)
    (local $var122 i32) (local $var123 i32) (local $var124 i32) (local $var125 i32)
    (local $var126 i32) (local $var127 i32) (local $var128 i32) (local $var129 i32)
    (local $var130 i32) (local $var131 i32) (local $var132 i32) (local $var133 i32)
    (local $var134 i32) (local $var135 i32) (local $var136 i32) (local $var137 i32)
    (local $var138 i32) (local $var139 i32) (local $var140 i32) (local $var141 i32)
    (local $var142 i32) (local $var143 i32) (local $var144 i32) (local $var145 i32)
    (local $var146 i32) (local $var147 i32) (local $var148 i32) (local $var149 i32)
    (local $var150 i32) (local $var151 i32) (local $var152 i32) (local $var153 i32)
    (local $var154 i32) (local $var155 i32) (local $var156 i32) (local $var157 i32)
    (local $var158 i32) (local $var159 i32) (local $var160 i32) (local $var161 i32)
    (local $var162 i32) (local $var163 i32) (local $var164 i32) (local $var165 i32)
    (local $var166 i32) (local $var167 i32) (local $var168 i32) (local $var169 i32)
    (local $var170 i32) (local $var171 i32) (local $var172 i32) (local $var173 i32)
    (local $var174 i32) (local $var175 i32) (local $var176 i32) (local $var177 i32)
    (local $var178 i32) (local $var179 i32) (local $var180 i32) (local $var181 i32)
    (local $var182 i32) (local $var183 i32) (local $var184 i32) (local $var185 i32)
    (local $var186 i32) (local $var187 i32) (local $var188 i32) (local $var189 i32)
    (local $var190 i32) (local $var191 i32) (local $var192 i32) (local $var193 i32)
    (local $var194 i32) (local $var195 i32) (local $var196 i32) (local $var197 i32)
    (local $var198 i32) (local $var199 i32) (local $var200 i32) (local $var201 i32)
    (local $var202 i32) (local $var203 i32) (local $var204 i32) (local $var205 i32)
    (local $var206 i32) (local $var207 i32) (local $var208 i32) (local $var209 i32)
    (local $var210 i32) (local $var211 i32) (local $var212 i32) (local $var213 i32)
    (local $var214 i32) (local $var215 i32) (local $var216 i32) (local $var217 i32)
    (local $var218 i32) (local $var219 i32) (local $var220 i32) (local $var221 i32)
    (local $var222 i32) (local $var223 i32) (local $var224 i32) (local $var225 i32)
    (local $var226 i32) (local $var227 i32) (local $var228 i32) (local $var229 i32)
    (local $var230 i32) (local $var231 i32) (local $var232 i32) (local $var233 i32)
    (local $var234 i32) (local $var235 i32) (local $var236 i32) (local $var237 i32)
    (local $var238 i32) (local $var239 i32) (local $var240 i32) (local $var241 i32)
    (local $var242 i32) (local $var243 i32) (local $var244 i32) (local $var245 i32)
    (local $var246 i32) (local $var247 i32) (local $var248 i32) (local $var249 i32)
    (local $var250 i32) (local $var251 i32) (local $var252 i32) (local $var253 i32)
    (local $var254 i32) (local $var255 i32) (local $var256 i32) (local $var257 i32)
    (local $var258 i32) (local $var259 i32) (local $var260 i32) (local $var261 i32)
    (local $var262 i32) (local $var263 i32) (local $var264 i32) (local $var265 i32)
    (local $var266 i32) (local $var267 i32) (local $var268 i32)
    
    global.get $global0
    local.set $var2
    i32.const 48
    local.set $var3
    local.get $var2
    local.get $var3
    i32.sub
    local.set $var4
    i32.const 0
    local.set $var5
    i32.const 15
    local.set $var6
    i32.const 20
    local.set $var7
    local.get $var4
    local.get $var0
    i32.store offset=44
    local.get $var4
    local.get $var1
    i32.store offset=40
    local.get $var4
    local.get $var7
    i32.store offset=36
    local.get $var4
    local.get $var6
    i32.store offset=32
    local.get $var4
    local.get $var5
    i32.store offset=28
    local.get $var4
    local.get $var5
    i32.store offset=24
    local.get $var4
    local.get $var5
    i32.store offset=20
    local.get $var4
    local.get $var5
    i32.store offset=16
    local.get $var4
    local.get $var5
    i32.store offset=12
    local.get $var4
    local.get $var5
    i32.store offset=8
    block $label0
      loop $label15
        i32.const 5
        local.set $var8
        local.get $var4
        i32.load offset=8
        local.set $var9
        local.get $var9
        local.set $var10
        local.get $var8
        local.set $var11
        local.get $var10
        local.get $var11
        i32.le_s
        local.set $var12
        local.get $var12
        local.set $var13
        local.get $var13
        i32.eqz
        br_if $label0
        i32.const 10000000
        local.set $var14
        local.get $var4
        i32.load offset=40
        local.set $var15
        local.get $var15
        local.set $var16
        local.get $var14
        local.set $var17
        local.get $var16
        local.get $var17
        i32.ge_s
        local.set $var18
        local.get $var18
        local.set $var19
        block $label1
          local.get $var19
          i32.eqz
          br_if $label1
          local.get $var4
          i32.load offset=40
          local.set $var20
          i32.const 2
          local.set $var21
          local.get $var20
          local.get $var21
          i32.div_s
          local.set $var22
          local.get $var4
          local.get $var22
          i32.store offset=40
        end $label1
        i32.const -10000000
        local.set $var23
        local.get $var4
        i32.load offset=40
        local.set $var24
        local.get $var24
        local.set $var25
        local.get $var23
        local.set $var26
        local.get $var25
        local.get $var26
        i32.le_s
        local.set $var27
        local.get $var27
        local.set $var28
        block $label2
          local.get $var28
          i32.eqz
          br_if $label2
          local.get $var4
          i32.load offset=40
          local.set $var29
          i32.const 2
          local.set $var30
          local.get $var29
          local.get $var30
          i32.div_s
          local.set $var31
          local.get $var4
          local.get $var31
          i32.store offset=40
        end $label2
        i32.const 10000000
        local.set $var32
        local.get $var4
        i32.load offset=44
        local.set $var33
        local.get $var33
        local.set $var34
        local.get $var32
        local.set $var35
        local.get $var34
        local.get $var35
        i32.ge_s
        local.set $var36
        local.get $var36
        local.set $var37
        block $label3
          local.get $var37
          i32.eqz
          br_if $label3
          local.get $var4
          i32.load offset=44
          local.set $var38
          i32.const 2
          local.set $var39
          local.get $var38
          local.get $var39
          i32.div_s
          local.set $var40
          local.get $var4
          local.get $var40
          i32.store offset=44
        end $label3
        i32.const -10000000
        local.set $var41
        local.get $var4
        i32.load offset=44
        local.set $var42
        local.get $var42
        local.set $var43
        local.get $var41
        local.set $var44
        local.get $var43
        local.get $var44
        i32.le_s
        local.set $var45
        local.get $var45
        local.set $var46
        block $label4
          local.get $var46
          i32.eqz
          br_if $label4
          local.get $var4
          i32.load offset=44
          local.set $var47
          i32.const 2
          local.set $var48
          local.get $var47
          local.get $var48
          i32.div_s
          local.set $var49
          local.get $var4
          local.get $var49
          i32.store offset=44
        end $label4
        i32.const 10000000
        local.set $var50
        local.get $var4
        i32.load offset=12
        local.set $var51
        local.get $var51
        local.set $var52
        local.get $var50
        local.set $var53
        local.get $var52
        local.get $var53
        i32.ge_s
        local.set $var54
        local.get $var54
        local.set $var55
        block $label5
          local.get $var55
          i32.eqz
          br_if $label5
          local.get $var4
          i32.load offset=12
          local.set $var56
          i32.const 2
          local.set $var57
          local.get $var56
          local.get $var57
          i32.div_s
          local.set $var58
          local.get $var4
          local.get $var58
          i32.store offset=12
        end $label5
        i32.const -10000000
        local.set $var59
        local.get $var4
        i32.load offset=12
        local.set $var60
        local.get $var60
        local.set $var61
        local.get $var59
        local.set $var62
        local.get $var61
        local.get $var62
        i32.le_s
        local.set $var63
        local.get $var63
        local.set $var64
        block $label6
          local.get $var64
          i32.eqz
          br_if $label6
          local.get $var4
          i32.load offset=12
          local.set $var65
          i32.const 2
          local.set $var66
          local.get $var65
          local.get $var66
          i32.div_s
          local.set $var67
          local.get $var4
          local.get $var67
          i32.store offset=12
        end $label6
        i32.const 10000000
        local.set $var68
        i32.const 32
        local.set $var69
        local.get $var4
        i32.load offset=44
        local.set $var70
        i32.const 16
        local.set $var71
        local.get $var70
        local.get $var71
        i32.div_s
        local.set $var72
        local.get $var4
        local.get $var72
        i32.store offset=28
        local.get $var4
        i32.load offset=44
        local.set $var73
        local.get $var4
        i32.load offset=40
        local.set $var74
        local.get $var73
        local.get $var74
        i32.and
        local.set $var75
        local.get $var4
        i32.load offset=32
        local.set $var76
        i32.const -1
        local.set $var77
        local.get $var76
        local.get $var77
        i32.xor
        local.set $var78
        local.get $var4
        i32.load offset=36
        local.set $var79
        local.get $var78
        local.get $var79
        i32.and
        local.set $var80
        local.get $var75
        local.get $var80
        i32.or
        local.set $var81
        local.get $var4
        local.get $var81
        i32.store offset=24
        local.get $var4
        i32.load offset=24
        local.set $var82
        i32.const 8
        local.set $var83
        local.get $var82
        local.get $var83
        i32.div_s
        local.set $var84
        local.get $var4
        local.get $var84
        i32.store offset=24
        local.get $var4
        i32.load offset=44
        local.set $var85
        local.get $var4
        i32.load offset=40
        local.set $var86
        local.get $var85
        local.get $var86
        i32.and
        local.set $var87
        local.get $var4
        i32.load offset=32
        local.set $var88
        local.get $var4
        i32.load offset=36
        local.set $var89
        i32.const -1
        local.set $var90
        local.get $var89
        local.get $var90
        i32.xor
        local.set $var91
        local.get $var88
        local.get $var91
        i32.and
        local.set $var92
        local.get $var87
        local.get $var92
        i32.or
        local.set $var93
        i32.const 8
        local.set $var94
        local.get $var93
        local.get $var94
        i32.div_s
        local.set $var95
        local.get $var4
        i32.load offset=24
        local.set $var96
        local.get $var96
        local.get $var95
        i32.add
        local.set $var97
        local.get $var4
        local.get $var97
        i32.store offset=24
        local.get $var4
        i32.load offset=36
        local.set $var98
        local.get $var4
        i32.load offset=32
        local.set $var99
        local.get $var98
        local.get $var99
        i32.xor
        local.set $var100
        local.get $var4
        i32.load offset=40
        local.set $var101
        local.get $var100
        local.get $var101
        i32.xor
        local.set $var102
        local.get $var4
        local.get $var102
        i32.store offset=20
        local.get $var4
        i32.load offset=20
        local.set $var103
        i32.const 9
        local.set $var104
        local.get $var103
        local.get $var104
        i32.div_s
        local.set $var105
        local.get $var4
        local.get $var105
        i32.store offset=20
        local.get $var4
        i32.load offset=44
        local.set $var106
        local.get $var4
        i32.load offset=36
        local.set $var107
        local.get $var106
        local.get $var107
        i32.shl
        local.set $var108
        local.get $var4
        i32.load offset=44
        local.set $var109
        local.get $var4
        i32.load offset=32
        local.set $var110
        local.get $var69
        local.get $var110
        i32.sub
        local.set $var111
        local.get $var109
        local.get $var111
        i32.shr_s
        local.set $var112
        local.get $var108
        local.get $var112
        i32.or
        local.set $var113
        local.get $var4
        local.get $var113
        i32.store offset=16
        local.get $var4
        i32.load offset=16
        local.set $var114
        local.get $var114
        local.set $var115
        local.get $var68
        local.set $var116
        local.get $var115
        local.get $var116
        i32.ge_s
        local.set $var117
        local.get $var117
        local.set $var118
        block $label7
          local.get $var118
          i32.eqz
          br_if $label7
          local.get $var4
          i32.load offset=16
          local.set $var119
          i32.const 4
          local.set $var120
          local.get $var119
          local.get $var120
          i32.div_s
          local.set $var121
          local.get $var4
          local.get $var121
          i32.store offset=16
        end $label7
        i32.const -10000000
        local.set $var122
        local.get $var4
        i32.load offset=16
        local.set $var123
        local.get $var123
        local.set $var124
        local.get $var122
        local.set $var125
        local.get $var124
        local.get $var125
        i32.le_s
        local.set $var126
        local.get $var126
        local.set $var127
        block $label8
          local.get $var127
          i32.eqz
          br_if $label8
          local.get $var4
          i32.load offset=16
          local.set $var128
          i32.const 4
          local.set $var129
          local.get $var128
          local.get $var129
          i32.div_s
          local.set $var130
          local.get $var4
          local.get $var130
          i32.store offset=16
        end $label8
        i32.const 10000000
        local.set $var131
        i32.const 32
        local.set $var132
        local.get $var4
        i32.load offset=16
        local.set $var133
        i32.const 16
        local.set $var134
        local.get $var133
        local.get $var134
        i32.div_s
        local.set $var135
        local.get $var4
        local.get $var135
        i32.store offset=16
        local.get $var4
        i32.load offset=44
        local.set $var136
        local.get $var4
        i32.load offset=40
        local.set $var137
        local.get $var4
        i32.load offset=32
        local.set $var138
        i32.const -1
        local.set $var139
        local.get $var138
        local.get $var139
        i32.xor
        local.set $var140
        local.get $var137
        local.get $var140
        i32.or
        local.set $var141
        local.get $var136
        local.get $var141
        i32.xor
        local.set $var142
        local.get $var4
        local.get $var142
        i32.store offset=12
        local.get $var4
        i32.load offset=44
        local.set $var143
        local.get $var4
        i32.load offset=40
        local.set $var144
        local.get $var4
        i32.load offset=32
        local.set $var145
        i32.const -1
        local.set $var146
        local.get $var145
        local.get $var146
        i32.xor
        local.set $var147
        local.get $var144
        local.get $var147
        i32.or
        local.set $var148
        local.get $var143
        local.get $var148
        i32.xor
        local.set $var149
        local.get $var4
        local.get $var149
        i32.store offset=44
        local.get $var4
        i32.load offset=44
        local.set $var150
        local.get $var4
        i32.load offset=40
        local.set $var151
        local.get $var150
        local.get $var151
        i32.and
        local.set $var152
        local.get $var4
        i32.load offset=32
        local.set $var153
        i32.const -1
        local.set $var154
        local.get $var153
        local.get $var154
        i32.xor
        local.set $var155
        local.get $var4
        i32.load offset=36
        local.set $var156
        local.get $var155
        local.get $var156
        i32.and
        local.set $var157
        local.get $var152
        local.get $var157
        i32.or
        local.set $var158
        local.get $var4
        local.get $var158
        i32.store offset=40
        local.get $var4
        i32.load offset=40
        local.set $var159
        local.get $var4
        i32.load offset=36
        local.set $var160
        local.get $var159
        local.get $var160
        i32.shl
        local.set $var161
        local.get $var4
        i32.load offset=44
        local.set $var162
        local.get $var4
        i32.load offset=32
        local.set $var163
        local.get $var132
        local.get $var163
        i32.sub
        local.set $var164
        local.get $var162
        local.get $var164
        i32.shr_s
        local.set $var165
        local.get $var161
        local.get $var165
        i32.or
        local.set $var166
        local.get $var4
        local.get $var166
        i32.store offset=36
        local.get $var4
        i32.load offset=36
        local.set $var167
        local.get $var167
        local.set $var168
        local.get $var131
        local.set $var169
        local.get $var168
        local.get $var169
        i32.ge_s
        local.set $var170
        local.get $var170
        local.set $var171
        block $label9
          local.get $var171
          i32.eqz
          br_if $label9
          local.get $var4
          i32.load offset=36
          local.set $var172
          i32.const 2
          local.set $var173
          local.get $var172
          local.get $var173
          i32.div_s
          local.set $var174
          local.get $var4
          local.get $var174
          i32.store offset=36
        end $label9
        i32.const -10000000
        local.set $var175
        local.get $var4
        i32.load offset=36
        local.set $var176
        local.get $var176
        local.set $var177
        local.get $var175
        local.set $var178
        local.get $var177
        local.get $var178
        i32.le_s
        local.set $var179
        local.get $var179
        local.set $var180
        block $label10
          local.get $var180
          i32.eqz
          br_if $label10
          local.get $var4
          i32.load offset=36
          local.set $var181
          i32.const 2
          local.set $var182
          local.get $var181
          local.get $var182
          i32.div_s
          local.set $var183
          local.get $var4
          local.get $var183
          i32.store offset=36
        end $label10
        i32.const 10000000
        local.set $var184
        i32.const 64
        local.set $var185
        local.get $var4
        i32.load offset=40
        local.set $var186
        local.get $var4
        i32.load offset=36
        local.set $var187
        local.get $var186
        local.get $var187
        i32.shl
        local.set $var188
        local.get $var4
        i32.load offset=44
        local.set $var189
        local.get $var4
        i32.load offset=32
        local.set $var190
        local.get $var185
        local.get $var190
        i32.sub
        local.set $var191
        local.get $var189
        local.get $var191
        i32.shr_s
        local.set $var192
        local.get $var188
        local.get $var192
        i32.or
        local.set $var193
        local.get $var4
        local.get $var193
        i32.store offset=36
        local.get $var4
        i32.load offset=36
        local.set $var194
        local.get $var194
        local.set $var195
        local.get $var184
        local.set $var196
        local.get $var195
        local.get $var196
        i32.ge_s
        local.set $var197
        local.get $var197
        local.set $var198
        block $label11
          local.get $var198
          i32.eqz
          br_if $label11
          local.get $var4
          i32.load offset=36
          local.set $var199
          i32.const 2
          local.set $var200
          local.get $var199
          local.get $var200
          i32.div_s
          local.set $var201
          local.get $var4
          local.get $var201
          i32.store offset=36
        end $label11
        i32.const -10000000
        local.set $var202
        local.get $var4
        i32.load offset=36
        local.set $var203
        local.get $var203
        local.set $var204
        local.get $var202
        local.set $var205
        local.get $var204
        local.get $var205
        i32.le_s
        local.set $var206
        local.get $var206
        local.set $var207
        block $label12
          local.get $var207
          i32.eqz
          br_if $label12
          local.get $var4
          i32.load offset=36
          local.set $var208
          i32.const 2
          local.set $var209
          local.get $var208
          local.get $var209
          i32.div_s
          local.set $var210
          local.get $var4
          local.get $var210
          i32.store offset=36
        end $label12
        i32.const 10000000
        local.set $var211
        local.get $var4
        i32.load offset=44
        local.set $var212
        local.get $var4
        i32.load offset=40
        local.set $var213
        local.get $var4
        i32.load offset=32
        local.set $var214
        i32.const -1
        local.set $var215
        local.get $var214
        local.get $var215
        i32.xor
        local.set $var216
        local.get $var213
        local.get $var216
        i32.or
        local.set $var217
        local.get $var212
        local.get $var217
        i32.xor
        local.set $var218
        local.get $var4
        local.get $var218
        i32.store offset=32
        local.get $var4
        i32.load offset=28
        local.set $var219
        local.get $var4
        i32.load offset=24
        local.set $var220
        local.get $var219
        local.get $var220
        i32.add
        local.set $var221
        local.get $var4
        i32.load offset=20
        local.set $var222
        local.get $var221
        local.get $var222
        i32.add
        local.set $var223
        local.get $var4
        i32.load offset=12
        local.set $var224
        local.get $var223
        local.get $var224
        i32.add
        local.set $var225
        local.get $var4
        i32.load offset=16
        local.set $var226
        local.get $var225
        local.get $var226
        i32.sub
        local.set $var227
        local.get $var4
        i32.load offset=40
        local.set $var228
        local.get $var227
        local.get $var228
        i32.add
        local.set $var229
        local.get $var4
        i32.load offset=44
        local.set $var230
        local.get $var229
        local.get $var230
        i32.sub
        local.set $var231
        local.get $var4
        i32.load offset=32
        local.set $var232
        local.get $var231
        local.get $var232
        i32.add
        local.set $var233
        local.get $var4
        local.get $var233
        i32.store offset=28
        local.get $var4
        i32.load offset=28
        local.set $var234
        local.get $var234
        local.set $var235
        local.get $var211
        local.set $var236
        local.get $var235
        local.get $var236
        i32.ge_s
        local.set $var237
        local.get $var237
        local.set $var238
        block $label13
          local.get $var238
          i32.eqz
          br_if $label13
          local.get $var4
          i32.load offset=28
          local.set $var239
          i32.const 2
          local.set $var240
          local.get $var239
          local.get $var240
          i32.div_s
          local.set $var241
          local.get $var4
          local.get $var241
          i32.store offset=28
        end $label13
        i32.const -10000000
        local.set $var242
        local.get $var4
        i32.load offset=28
        local.set $var243
        local.get $var243
        local.set $var244
        local.get $var242
        local.set $var245
        local.get $var244
        local.get $var245
        i32.le_s
        local.set $var246
        local.get $var246
        local.set $var247
        block $label14
          local.get $var247
          i32.eqz
          br_if $label14
          local.get $var4
          i32.load offset=28
          local.set $var248
          i32.const 2
          local.set $var249
          local.get $var248
          local.get $var249
          i32.div_s
          local.set $var250
          local.get $var4
          local.get $var250
          i32.store offset=28
        end $label14
        local.get $var4
        i32.load offset=8
        local.set $var251
        i32.const 1
        local.set $var252
        local.get $var251
        local.get $var252
        i32.add
        local.set $var253
        local.get $var4
        local.get $var253
        i32.store offset=8
        br $label15
      end $label15
    end $label0
    local.get $var4
    i32.load offset=28
    local.set $var254
    local.get $var4
    i32.load offset=24
    local.set $var255
    local.get $var254
    local.get $var255
    i32.add
    local.set $var256
    i32.const 2
    local.set $var257
    local.get $var256
    local.get $var257
    i32.div_s
    local.set $var258
    local.get $var4
    i32.load offset=12
    local.set $var259
    local.get $var258
    local.get $var259
    i32.add
    local.set $var260
    local.get $var4
    i32.load offset=16
    local.set $var261
    local.get $var260
    local.get $var261
    i32.sub
    local.set $var262
    local.get $var4
    i32.load offset=40
    local.set $var263
    local.get $var262
    local.get $var263
    i32.add
    local.set $var264
    local.get $var4
    i32.load offset=44
    local.set $var265
    local.get $var264
    local.get $var265
    i32.add
    local.set $var266
    i32.const 2
    local.set $var267
    local.get $var266
    local.get $var267
    i32.div_s
    local.set $var268
    local.get $var268
    return
  )
)