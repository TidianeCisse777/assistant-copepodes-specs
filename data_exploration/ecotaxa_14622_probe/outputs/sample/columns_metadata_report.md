# Colonnes EcoTaxa - projet 14622

Extraction metadata-only : aucune ligne objet n'est telechargee.

## Projet

- Projet : LOKI_ArcticNet_2015 (`14622`)
- Instrument : Loki
- Objets annonces : 1687393.0
- Pourcentage valide : 10.078031614449035
- Pourcentage classifie : 100.0

## Comptes de colonnes

- standard : 23
- classification_display : 4
- object_free : 205
- sample : 18
- acquisition : 29
- process : 2

## Colonnes par categorie

### classification_display

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `fre.equivalent_diameter_area` |  | ESD | Champ libre objet affiche dans la liste de classification sous le libelle ESD. |
| `fre.axis_major_length` |  | Major | Champ libre objet affiche dans la liste de classification sous le libelle Major. |
| `fre.axis_minor_length` |  | Minor | Champ libre objet affiche dans la liste de classification sous le libelle Minor. |
| `fre.Depth min` |  | Depth | Champ libre objet affiche dans la liste de classification sous le libelle Depth. |

### object

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `obj.orig_id` |  | Identifiant original de l'objet | Identifiant original de l'objet |
| `obj.latitude` |  | Latitude de l'objet | Latitude de l'objet |
| `obj.longitude` |  | Longitude de l'objet | Longitude de l'objet |
| `obj.objdate` |  | Date de l'objet | Date de l'objet |
| `obj.objtime` |  | Heure de l'objet | Heure de l'objet |
| `obj.depth_min` |  | Profondeur minimale | Profondeur minimale |
| `obj.depth_max` |  | Profondeur maximale | Profondeur maximale |
| `obj.classif_qual` |  | Statut de classification | Statut de classification |
| `obj.classif_id` |  | Identifiant taxonomique retenu | Identifiant taxonomique retenu |
| `obj.classif_who` |  | Validateur ou classificateur | Validateur ou classificateur |
| `obj.classif_when` |  | Date de classification | Date de classification |
| `obj.classif_auto_id` |  | Identifiant taxonomique automatique | Identifiant taxonomique automatique |
| `obj.classif_auto_score` |  | Score de classification automatique | Score de classification automatique |
| `obj.classif_auto_when` |  | Date de classification automatique | Date de classification automatique |
| `obj.complement_info` |  | Information complementaire objet | Information complementaire objet |
| `obj.object_link` |  | Lien objet | Lien objet |
| `obj.random_value` |  | Valeur aleatoire interne | Valeur aleatoire interne |
| `obj.sunpos` |  | Position solaire calculee | Position solaire calculee |

### taxonomy

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `txo.display_name` |  | Nom taxonomique affiche | Nom taxonomique affiche |
| `txo.name` |  | Nom taxonomique brut | Nom taxonomique brut |
| `txo.id` |  | Identifiant taxonomique EcoTaxa | Identifiant taxonomique EcoTaxa |
| `txo.parent_id` |  | Identifiant du parent taxonomique | Identifiant du parent taxonomique |
| `txo.aphia_id` |  | Identifiant Aphia/WoRMS si disponible | Identifiant Aphia/WoRMS si disponible |

### object_free

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `fre.frame_ms` | n01 | frame ms | Champ libre object_free fourni par EcoTaxa, stocke dans n01. |
| `fre.frame_vignette_number` | n02 | frame vignette number | Champ libre object_free fourni par EcoTaxa, stocke dans n02. |
| `fre.vignette_x_pos` | n03 | vignette x pos | Champ libre object_free fourni par EcoTaxa, stocke dans n03. |
| `fre.vignette_y_pos` | n04 | vignette y pos | Champ libre object_free fourni par EcoTaxa, stocke dans n04. |
| `fre.orig_img_bmp_file_size` | n05 | orig img bmp file size | Champ libre object_free fourni par EcoTaxa, stocke dans n05. |
| `fre.image_height` | n06 | image height | Champ libre object_free fourni par EcoTaxa, stocke dans n06. |
| `fre.image_width` | n07 | image width | Champ libre object_free fourni par EcoTaxa, stocke dans n07. |
| `fre.image_pixel_low_extrema` | n08 | image pixel low extrema | Champ libre object_free fourni par EcoTaxa, stocke dans n08. |
| `fre.image_pixel_high_extrema` | n09 | image pixel high extrema | Champ libre object_free fourni par EcoTaxa, stocke dans n09. |
| `fre.image_pixel_count` | n10 | image pixel count | Champ libre object_free fourni par EcoTaxa, stocke dans n10. |
| `fre.moments_weighted-0-1` | n100 | moments weighted-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n100. |
| `fre.moments_weighted-0-2` | n101 | moments weighted-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n101. |
| `fre.moments_weighted-0-3` | n102 | moments weighted-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n102. |
| `fre.moments_weighted-1-0` | n103 | moments weighted-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n103. |
| `fre.moments_weighted-1-1` | n104 | moments weighted-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n104. |
| `fre.moments_weighted-1-2` | n105 | moments weighted-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n105. |
| `fre.moments_weighted-1-3` | n106 | moments weighted-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n106. |
| `fre.moments_weighted-2-0` | n107 | moments weighted-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n107. |
| `fre.moments_weighted-2-1` | n108 | moments weighted-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n108. |
| `fre.moments_weighted-2-2` | n109 | moments weighted-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n109. |
| `fre.image_pixel_int_mean` | n11 | image pixel int mean | Champ libre object_free fourni par EcoTaxa, stocke dans n11. |
| `fre.moments_weighted-2-3` | n110 | moments weighted-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n110. |
| `fre.moments_weighted-3-0` | n111 | moments weighted-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n111. |
| `fre.moments_weighted-3-1` | n112 | moments weighted-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n112. |
| `fre.moments_weighted-3-2` | n113 | moments weighted-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n113. |
| `fre.moments_weighted-3-3` | n114 | moments weighted-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n114. |
| `fre.moments_weighted_central-0-0` | n115 | moments weighted central-0-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n115. |
| `fre.moments_weighted_central-0-1` | n116 | moments weighted central-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n116. |
| `fre.moments_weighted_central-0-2` | n117 | moments weighted central-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n117. |
| `fre.moments_weighted_central-0-3` | n118 | moments weighted central-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n118. |
| `fre.moments_weighted_central-1-0` | n119 | moments weighted central-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n119. |
| `fre.image_pixel_int_variance` | n12 | image pixel int variance | Champ libre object_free fourni par EcoTaxa, stocke dans n12. |
| `fre.moments_weighted_central-1-1` | n120 | moments weighted central-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n120. |
| `fre.moments_weighted_central-1-2` | n121 | moments weighted central-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n121. |
| `fre.moments_weighted_central-1-3` | n122 | moments weighted central-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n122. |
| `fre.moments_weighted_central-2-0` | n123 | moments weighted central-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n123. |
| `fre.moments_weighted_central-2-1` | n124 | moments weighted central-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n124. |
| `fre.moments_weighted_central-2-2` | n125 | moments weighted central-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n125. |
| `fre.moments_weighted_central-2-3` | n126 | moments weighted central-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n126. |
| `fre.moments_weighted_central-3-0` | n127 | moments weighted central-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n127. |
| `fre.moments_weighted_central-3-1` | n128 | moments weighted central-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n128. |
| `fre.moments_weighted_central-3-2` | n129 | moments weighted central-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n129. |
| `fre.image_pixel_int_stddev` | n13 | image pixel int stddev | Champ libre object_free fourni par EcoTaxa, stocke dans n13. |
| `fre.moments_weighted_central-3-3` | n130 | moments weighted central-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n130. |
| `fre.moments_weighted_hu-0` | n131 | moments weighted hu-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n131. |
| `fre.moments_weighted_hu-1` | n132 | moments weighted hu-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n132. |
| `fre.moments_weighted_hu-2` | n133 | moments weighted hu-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n133. |
| `fre.moments_weighted_hu-3` | n134 | moments weighted hu-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n134. |
| `fre.moments_weighted_hu-4` | n135 | moments weighted hu-4 | Champ libre object_free fourni par EcoTaxa, stocke dans n135. |
| `fre.moments_weighted_hu-5` | n136 | moments weighted hu-5 | Champ libre object_free fourni par EcoTaxa, stocke dans n136. |
| `fre.moments_weighted_hu-6` | n137 | moments weighted hu-6 | Champ libre object_free fourni par EcoTaxa, stocke dans n137. |
| `fre.moments_weighted_normalized-0-2` | n138 | moments weighted normalized-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n138. |
| `fre.moments_weighted_normalized-0-3` | n139 | moments weighted normalized-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n139. |
| `fre.area` | n14 | area | Champ libre object_free fourni par EcoTaxa, stocke dans n14. |
| `fre.moments_weighted_normalized-1-1` | n140 | moments weighted normalized-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n140. |
| `fre.moments_weighted_normalized-1-2` | n141 | moments weighted normalized-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n141. |
| `fre.moments_weighted_normalized-1-3` | n142 | moments weighted normalized-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n142. |
| `fre.moments_weighted_normalized-2-0` | n143 | moments weighted normalized-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n143. |
| `fre.moments_weighted_normalized-2-1` | n144 | moments weighted normalized-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n144. |
| `fre.moments_weighted_normalized-2-2` | n145 | moments weighted normalized-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n145. |
| `fre.moments_weighted_normalized-2-3` | n146 | moments weighted normalized-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n146. |
| `fre.moments_weighted_normalized-3-0` | n147 | moments weighted normalized-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n147. |
| `fre.moments_weighted_normalized-3-1` | n148 | moments weighted normalized-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n148. |
| `fre.moments_weighted_normalized-3-2` | n149 | moments weighted normalized-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n149. |
| `fre.area_bbox` | n15 | area bbox | Champ libre object_free fourni par EcoTaxa, stocke dans n15. |
| `fre.moments_weighted_normalized-3-3` | n150 | moments weighted normalized-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n150. |
| `fre.orientation` | n151 | orientation | Champ libre object_free fourni par EcoTaxa, stocke dans n151. |
| `fre.perimeter` | n152 | perimeter | Champ libre object_free fourni par EcoTaxa, stocke dans n152. |
| `fre.perimeter_crofton` | n153 | perimeter crofton | Champ libre object_free fourni par EcoTaxa, stocke dans n153. |
| `fre.solidity` | n154 | solidity | Champ libre object_free fourni par EcoTaxa, stocke dans n154. |
| `fre.threshold` | n155 | threshold | Champ libre object_free fourni par EcoTaxa, stocke dans n155. |
| `fre.trimmed_masked_image_numb_of_regions` | n156 | trimmed masked image numb of regions | Champ libre object_free fourni par EcoTaxa, stocke dans n156. |
| `fre.trimmed_mask_numb_of_regions` | n157 | trimmed mask numb of regions | Champ libre object_free fourni par EcoTaxa, stocke dans n157. |
| `fre.trimmed_labeled_mask_numb_of_regions` | n158 | trimmed labeled mask numb of regions | Champ libre object_free fourni par EcoTaxa, stocke dans n158. |
| `fre.log_moments_central-0-1` | n159 | log moments central-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n159. |
| `fre.area_convex` | n16 | area convex | Champ libre object_free fourni par EcoTaxa, stocke dans n16. |
| `fre.log_moments_central-1-0` | n160 | log moments central-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n160. |
| `fre.log_moments_hu-1` | n161 | log moments hu-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n161. |
| `fre.log_moments_hu-2` | n162 | log moments hu-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n162. |
| `fre.log_moments_hu-3` | n163 | log moments hu-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n163. |
| `fre.log_moments_hu-4` | n164 | log moments hu-4 | Champ libre object_free fourni par EcoTaxa, stocke dans n164. |
| `fre.log_moments_hu-5` | n165 | log moments hu-5 | Champ libre object_free fourni par EcoTaxa, stocke dans n165. |
| `fre.log_moments_hu-6` | n166 | log moments hu-6 | Champ libre object_free fourni par EcoTaxa, stocke dans n166. |
| `fre.log_moments_normalized-0-3` | n167 | log moments normalized-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n167. |
| `fre.log_moments_normalized-1-1` | n168 | log moments normalized-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n168. |
| `fre.log_moments_normalized-1-2` | n169 | log moments normalized-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n169. |
| `fre.area_filled` | n17 | area filled | Champ libre object_free fourni par EcoTaxa, stocke dans n17. |
| `fre.log_moments_normalized-1-3` | n170 | log moments normalized-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n170. |
| `fre.log_moments_normalized-2-1` | n171 | log moments normalized-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n171. |
| `fre.log_moments_normalized-2-2` | n172 | log moments normalized-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n172. |
| `fre.log_moments_normalized-2-3` | n173 | log moments normalized-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n173. |
| `fre.log_moments_normalized-3-0` | n174 | log moments normalized-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n174. |
| `fre.log_moments_normalized-3-1` | n175 | log moments normalized-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n175. |
| `fre.log_moments_normalized-3-2` | n176 | log moments normalized-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n176. |
| `fre.log_moments_normalized-3-3` | n177 | log moments normalized-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n177. |
| `fre.log_moments_weighted_central-0-1` | n178 | log moments weighted central-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n178. |
| `fre.log_moments_weighted_central-1-0` | n179 | log moments weighted central-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n179. |
| `fre.axis_major_length` | n18 | axis major length | Champ libre object_free fourni par EcoTaxa, stocke dans n18. |
| `fre.log_moments_weighted_hu-0` | n180 | log moments weighted hu-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n180. |
| `fre.log_moments_weighted_hu-1` | n181 | log moments weighted hu-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n181. |
| `fre.log_moments_weighted_hu-2` | n182 | log moments weighted hu-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n182. |
| `fre.log_moments_weighted_hu-3` | n183 | log moments weighted hu-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n183. |
| `fre.log_moments_weighted_hu-4` | n184 | log moments weighted hu-4 | Champ libre object_free fourni par EcoTaxa, stocke dans n184. |
| `fre.log_moments_weighted_hu-5` | n185 | log moments weighted hu-5 | Champ libre object_free fourni par EcoTaxa, stocke dans n185. |
| `fre.log_moments_weighted_hu-6` | n186 | log moments weighted hu-6 | Champ libre object_free fourni par EcoTaxa, stocke dans n186. |
| `fre.log_moments_weighted_normalized-0-2` | n187 | log moments weighted normalized-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n187. |
| `fre.log_moments_weighted_normalized-0-3` | n188 | log moments weighted normalized-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n188. |
| `fre.log_moments_weighted_normalized-1-1` | n189 | log moments weighted normalized-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n189. |
| `fre.axis_minor_length` | n19 | axis minor length | Champ libre object_free fourni par EcoTaxa, stocke dans n19. |
| `fre.log_moments_weighted_normalized-1-2` | n190 | log moments weighted normalized-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n190. |
| `fre.log_moments_weighted_normalized-1-3` | n191 | log moments weighted normalized-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n191. |
| `fre.log_moments_weighted_normalized-2-0` | n192 | log moments weighted normalized-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n192. |
| `fre.log_moments_weighted_normalized-2-1` | n193 | log moments weighted normalized-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n193. |
| `fre.log_moments_weighted_normalized-2-2` | n194 | log moments weighted normalized-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n194. |
| `fre.log_moments_weighted_normalized-2-3` | n195 | log moments weighted normalized-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n195. |
| `fre.log_moments_weighted_normalized-3-0` | n196 | log moments weighted normalized-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n196. |
| `fre.log_moments_weighted_normalized-3-1` | n197 | log moments weighted normalized-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n197. |
| `fre.log_moments_weighted_normalized-3-2` | n198 | log moments weighted normalized-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n198. |
| `fre.log_moments_weighted_normalized-3-3` | n199 | log moments weighted normalized-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n199. |
| `fre.bbox-0` | n20 | bbox-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n20. |
| `fre.double_position` | n200 | double position | Champ libre object_free fourni par EcoTaxa, stocke dans n200. |
| `fre.total_doubles` | n201 | total doubles | Champ libre object_free fourni par EcoTaxa, stocke dans n201. |
| `fre.bbox-1` | n21 | bbox-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n21. |
| `fre.bbox-2` | n22 | bbox-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n22. |
| `fre.bbox-3` | n23 | bbox-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n23. |
| `fre.centroid-0` | n24 | centroid-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n24. |
| `fre.centroid-1` | n25 | centroid-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n25. |
| `fre.centroid_local-0` | n26 | centroid local-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n26. |
| `fre.centroid_local-1` | n27 | centroid local-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n27. |
| `fre.centroid_weighted-0` | n28 | centroid weighted-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n28. |
| `fre.centroid_weighted-1` | n29 | centroid weighted-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n29. |
| `fre.centroid_weighted_local-0` | n30 | centroid weighted local-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n30. |
| `fre.centroid_weighted_local-1` | n31 | centroid weighted local-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n31. |
| `fre.eccentricity` | n32 | eccentricity | Champ libre object_free fourni par EcoTaxa, stocke dans n32. |
| `fre.equivalent_diameter_area` | n33 | equivalent diameter area | Champ libre object_free fourni par EcoTaxa, stocke dans n33. |
| `fre.euler_number` | n34 | euler number | Champ libre object_free fourni par EcoTaxa, stocke dans n34. |
| `fre.extent` | n35 | extent | Champ libre object_free fourni par EcoTaxa, stocke dans n35. |
| `fre.feret_diameter_max` | n36 | feret diameter max | Champ libre object_free fourni par EcoTaxa, stocke dans n36. |
| `fre.inertia_tensor-0-0` | n37 | inertia tensor-0-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n37. |
| `fre.inertia_tensor-0-1` | n38 | inertia tensor-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n38. |
| `fre.inertia_tensor-1-0` | n39 | inertia tensor-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n39. |
| `fre.inertia_tensor-1-1` | n40 | inertia tensor-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n40. |
| `fre.inertia_tensor_eigvals-0` | n41 | inertia tensor eigvals-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n41. |
| `fre.inertia_tensor_eigvals-1` | n42 | inertia tensor eigvals-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n42. |
| `fre.intensity_max` | n43 | intensity max | Champ libre object_free fourni par EcoTaxa, stocke dans n43. |
| `fre.intensity_mean` | n44 | intensity mean | Champ libre object_free fourni par EcoTaxa, stocke dans n44. |
| `fre.intensity_min` | n45 | intensity min | Champ libre object_free fourni par EcoTaxa, stocke dans n45. |
| `fre.label_id_number` | n46 | label id number | Champ libre object_free fourni par EcoTaxa, stocke dans n46. |
| `fre.moments-0-0` | n47 | moments-0-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n47. |
| `fre.moments-0-1` | n48 | moments-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n48. |
| `fre.moments-0-2` | n49 | moments-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n49. |
| `fre.moments-0-3` | n50 | moments-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n50. |
| `fre.moments-1-0` | n51 | moments-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n51. |
| `fre.moments-1-1` | n52 | moments-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n52. |
| `fre.moments-1-2` | n53 | moments-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n53. |
| `fre.moments-1-3` | n54 | moments-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n54. |
| `fre.moments-2-0` | n55 | moments-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n55. |
| `fre.moments-2-1` | n56 | moments-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n56. |
| `fre.moments-2-2` | n57 | moments-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n57. |
| `fre.moments-2-3` | n58 | moments-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n58. |
| `fre.moments-3-0` | n59 | moments-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n59. |
| `fre.moments-3-1` | n60 | moments-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n60. |
| `fre.moments-3-2` | n61 | moments-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n61. |
| `fre.moments-3-3` | n62 | moments-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n62. |
| `fre.moments_central-0-0` | n63 | moments central-0-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n63. |
| `fre.moments_central-0-1` | n64 | moments central-0-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n64. |
| `fre.moments_central-0-2` | n65 | moments central-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n65. |
| `fre.moments_central-0-3` | n66 | moments central-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n66. |
| `fre.moments_central-1-0` | n67 | moments central-1-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n67. |
| `fre.moments_central-1-1` | n68 | moments central-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n68. |
| `fre.moments_central-1-2` | n69 | moments central-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n69. |
| `fre.moments_central-1-3` | n70 | moments central-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n70. |
| `fre.moments_central-2-0` | n71 | moments central-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n71. |
| `fre.moments_central-2-1` | n72 | moments central-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n72. |
| `fre.moments_central-2-2` | n73 | moments central-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n73. |
| `fre.moments_central-2-3` | n74 | moments central-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n74. |
| `fre.moments_central-3-0` | n75 | moments central-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n75. |
| `fre.moments_central-3-1` | n76 | moments central-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n76. |
| `fre.moments_central-3-2` | n77 | moments central-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n77. |
| `fre.moments_central-3-3` | n78 | moments central-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n78. |
| `fre.moments_hu-0` | n79 | moments hu-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n79. |
| `fre.moments_hu-1` | n80 | moments hu-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n80. |
| `fre.moments_hu-2` | n81 | moments hu-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n81. |
| `fre.moments_hu-3` | n82 | moments hu-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n82. |
| `fre.moments_hu-4` | n83 | moments hu-4 | Champ libre object_free fourni par EcoTaxa, stocke dans n83. |
| `fre.moments_hu-5` | n84 | moments hu-5 | Champ libre object_free fourni par EcoTaxa, stocke dans n84. |
| `fre.moments_hu-6` | n85 | moments hu-6 | Champ libre object_free fourni par EcoTaxa, stocke dans n85. |
| `fre.moments_normalized-0-2` | n86 | moments normalized-0-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n86. |
| `fre.moments_normalized-0-3` | n87 | moments normalized-0-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n87. |
| `fre.moments_normalized-1-1` | n88 | moments normalized-1-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n88. |
| `fre.moments_normalized-1-2` | n89 | moments normalized-1-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n89. |
| `fre.moments_normalized-1-3` | n90 | moments normalized-1-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n90. |
| `fre.moments_normalized-2-0` | n91 | moments normalized-2-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n91. |
| `fre.moments_normalized-2-1` | n92 | moments normalized-2-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n92. |
| `fre.moments_normalized-2-2` | n93 | moments normalized-2-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n93. |
| `fre.moments_normalized-2-3` | n94 | moments normalized-2-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n94. |
| `fre.moments_normalized-3-0` | n95 | moments normalized-3-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n95. |
| `fre.moments_normalized-3-1` | n96 | moments normalized-3-1 | Champ libre object_free fourni par EcoTaxa, stocke dans n96. |
| `fre.moments_normalized-3-2` | n97 | moments normalized-3-2 | Champ libre object_free fourni par EcoTaxa, stocke dans n97. |
| `fre.moments_normalized-3-3` | n98 | moments normalized-3-3 | Champ libre object_free fourni par EcoTaxa, stocke dans n98. |
| `fre.moments_weighted-0-0` | n99 | moments weighted-0-0 | Champ libre object_free fourni par EcoTaxa, stocke dans n99. |
| `fre.double_prediction` | t01 | double prediction | Champ libre object_free fourni par EcoTaxa, stocke dans t01. |
| `fre.double_validation_status` | t02 | double validation status | Champ libre object_free fourni par EcoTaxa, stocke dans t02. |
| `fre.double_probability` | t03 | double probability | Champ libre object_free fourni par EcoTaxa, stocke dans t03. |
| `fre.double_of` | t04 | double of | Champ libre object_free fourni par EcoTaxa, stocke dans t04. |

### sample

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `sample.station_name` | t01 | station name | Champ libre sample fourni par EcoTaxa, stocke dans t01. |
| `sample.deployment_date_start` | t02 | deployment date start | Champ libre sample fourni par EcoTaxa, stocke dans t02. |
| `sample.deployment_time_start` | t03 | deployment time start | Champ libre sample fourni par EcoTaxa, stocke dans t03. |
| `sample.deployment_datetime_end` | t04 | deployment datetime end | Champ libre sample fourni par EcoTaxa, stocke dans t04. |
| `sample.gear` | t05 | gear | Champ libre sample fourni par EcoTaxa, stocke dans t05. |
| `sample.tow_type` | t06 | tow type | Champ libre sample fourni par EcoTaxa, stocke dans t06. |
| `sample.cast_number` | t07 | cast number | Champ libre sample fourni par EcoTaxa, stocke dans t07. |
| `sample.bottom_depth` | t08 | bottom depth | Champ libre sample fourni par EcoTaxa, stocke dans t08. |
| `sample.latitude` | t09 | latitude | Champ libre sample fourni par EcoTaxa, stocke dans t09. |
| `sample.longitude` | t10 | longitude | Champ libre sample fourni par EcoTaxa, stocke dans t10. |
| `sample.deployment_comments` | t11 | deployment comments | Champ libre sample fourni par EcoTaxa, stocke dans t11. |
| `sample.gear_net_id` | t12 | gear net id | Champ libre sample fourni par EcoTaxa, stocke dans t12. |
| `sample.net_mesh_size` | t13 | net mesh size | Champ libre sample fourni par EcoTaxa, stocke dans t13. |
| `sample.net_mouth_aperture` | t14 | net mouth aperture | Champ libre sample fourni par EcoTaxa, stocke dans t14. |
| `sample.max_net_sampling_depth` | t15 | max net sampling depth | Champ libre sample fourni par EcoTaxa, stocke dans t15. |
| `sample.min_net_sampling_depth` | t16 | min net sampling depth | Champ libre sample fourni par EcoTaxa, stocke dans t16. |
| `sample.deployment_datetime_start` | t17 | deployment datetime start | Champ libre sample fourni par EcoTaxa, stocke dans t17. |
| `sample.deployment_time_start_str` | t18 | deployment time start str | Champ libre sample fourni par EcoTaxa, stocke dans t18. |

### acquisition

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `acq.original_telemetry_profil_folder` | t01 | original telemetry profil folder | Champ libre acquisition fourni par EcoTaxa, stocke dans t01. |
| `acq.vprm version` | t02 | vprm version | Champ libre acquisition fourni par EcoTaxa, stocke dans t02. |
| `acq.sound_velocity` | t03 | sound velocity | Champ libre acquisition fourni par EcoTaxa, stocke dans t03. |
| `acq.density_ctd` | t04 | density ctd | Champ libre acquisition fourni par EcoTaxa, stocke dans t04. |
| `acq.temperature_ctd` | t05 | temperature ctd | Champ libre acquisition fourni par EcoTaxa, stocke dans t05. |
| `acq.conductivity_ctd` | t06 | conductivity ctd | Champ libre acquisition fourni par EcoTaxa, stocke dans t06. |
| `acq.salinity_ctd` | t07 | salinity ctd | Champ libre acquisition fourni par EcoTaxa, stocke dans t07. |
| `acq.oxygen_concent` | t08 | oxygen concent | Champ libre acquisition fourni par EcoTaxa, stocke dans t08. |
| `acq.oxygen_saturation` | t09 | oxygen saturation | Champ libre acquisition fourni par EcoTaxa, stocke dans t09. |
| `acq.oxygen_temperature` | t10 | oxygen temperature | Champ libre acquisition fourni par EcoTaxa, stocke dans t10. |
| `acq.loki_temperature` | t11 | loki temperature | Champ libre acquisition fourni par EcoTaxa, stocke dans t11. |
| `acq.loki_voltage` | t12 | loki voltage | Champ libre acquisition fourni par EcoTaxa, stocke dans t12. |
| `acq.status_acquire` | t13 | status acquire | Champ libre acquisition fourni par EcoTaxa, stocke dans t13. |
| `acq.speed` | t14 | speed | Champ libre acquisition fourni par EcoTaxa, stocke dans t14. |
| `acq.pitch` | t15 | pitch | Champ libre acquisition fourni par EcoTaxa, stocke dans t15. |
| `acq.roll` | t16 | roll | Champ libre acquisition fourni par EcoTaxa, stocke dans t16. |
| `acq.fluo1` | t17 | fluo1 | Champ libre acquisition fourni par EcoTaxa, stocke dans t17. |
| `acq.fluo2` | t18 | fluo2 | Champ libre acquisition fourni par EcoTaxa, stocke dans t18. |
| `acq.fluo3` | t19 | fluo3 | Champ libre acquisition fourni par EcoTaxa, stocke dans t19. |
| `acq.fluo4` | t20 | fluo4 | Champ libre acquisition fourni par EcoTaxa, stocke dans t20. |
| `acq.pressure_sensor_press` | t21 | pressure sensor press | Champ libre acquisition fourni par EcoTaxa, stocke dans t21. |
| `acq.pressure_sensor_temp` | t22 | pressure sensor temp | Champ libre acquisition fourni par EcoTaxa, stocke dans t22. |
| `acq.camera_status` | t23 | camera status | Champ libre acquisition fourni par EcoTaxa, stocke dans t23. |
| `acq.vprcl_status` | t24 | vprcl status | Champ libre acquisition fourni par EcoTaxa, stocke dans t24. |
| `acq.vprcl_picture_number` | t25 | vprcl picture number | Champ libre acquisition fourni par EcoTaxa, stocke dans t25. |
| `acq.vprcl_framerate` | t26 | vprcl framerate | Champ libre acquisition fourni par EcoTaxa, stocke dans t26. |
| `acq.raw_depth` | t27 | raw depth | Champ libre acquisition fourni par EcoTaxa, stocke dans t27. |
| `acq.depth_outlier` | t28 | depth outlier | Champ libre acquisition fourni par EcoTaxa, stocke dans t28. |
| `acq.pixel_um_size` | t29 | pixel um size | Champ libre acquisition fourni par EcoTaxa, stocke dans t29. |

### process

| Champ | Slot | Libelle | Definition |
|---|---:|---|---|
| `process.footer_height_px` | t01 | footer height px | Champ libre process fourni par EcoTaxa, stocke dans t01. |
| `process.python_img_feats_library` | t02 | python img feats library | Champ libre process fourni par EcoTaxa, stocke dans t02. |
