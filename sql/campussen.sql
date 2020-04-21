drop table if exists campus CASCADE;
create table campus(
	 id serial primary key,
	 name varchar(255),
	 category varchar(25),
	 latitude float8,
	 longitude float8
);

insert into campus
values (default, 'Academy Fine Arts De Verviers', 'college', 50.5908603, 5.86585700000001);

insert into campus
values (default, 'Academy Royale Des Beaux-Arts De Liège Center Secondary Education Léonard Defrance', 'college', 50.6464882, 5.569031);

insert into campus
values (default, 'Académie des Beaux-Arts', 'college', 50.520586, 5.23963179999998);

insert into campus
values (default, 'AP Hogeschool - Campus Dambruggestraat', 'college', 51.22917, 4.42137);

insert into campus
values (default, 'AP Hogeschool - Campus Keizerstraat', 'college', 51.22167, 4.40641);

insert into campus
values (default, 'AP Hogeschool - Campus Kronenburg', 'college', 51.2122, 4.39954);

insert into campus
values (default, 'AP Hogeschool - Campus Lange Nieuwstraat', 'college', 51.21946, 4.4119816);

insert into campus
values (default, 'AP Hogeschool - Campus Meistraat', 'college', 51.21639, 4.41103);

insert into campus
values (default, 'AP Hogeschool - Campus Spoor Noord - Ellermanstraat', 'college', 51.23037, 4.41603);

insert into campus
values (default, 'AP Hogeschool - Campus Spoor Noord - Lichttoren', 'college', 51.23025, 4.41846);

insert into campus
values (default, 'AP Hogeschool - Campus Spoor Noord - Noorderplaats', 'college', 51.23036, 4.41379);

insert into campus
values (default, 'AP Hogeschool - Campus Zuid ', 'college', 51.20897, 4.39707);

insert into campus
values (default, 'AP Hogeschool - Campus deSingel', 'college', 51.19289, 4.40418);

insert into campus
values (default, 'APB - Campus Vesta', 'college', 51.17458, 4.62255);

insert into campus
values (default, 'Academy Des Beaux-Arts', 'college', 49.6733113, 5.81749790000003);

insert into campus
values (default, 'Académie Constantin Meunier', 'college', 50.835403, 4.395971);

insert into campus
values (default, 'Académie Royale des Beaux-Arts de Bruxelles-Ecole', 'college', 50.84362, 4.34738);

insert into campus
values (default, 'Antwerp Management School', 'college', 51.220634, 4.4106297);

insert into campus
values (default, 'Arbeidershogeschool - École Ouvrière Supérieure', 'college', 50.81768, 4.37551);

insert into campus
values (default, 'Arteveldehogeschool - Campus Brusselsepoortstraat', 'college', 51.0428917, 3.73799819999999);

insert into campus
values (default, 'Arteveldehogeschool - Campus Goudstraat', 'college', 51.0599405, 3.72804759999997);

insert into campus
values (default, 'Arteveldehogeschool - Campus Hoogpoort', 'college', 51.0554832, 3.72335709999993);

insert into campus
values (default, 'Arteveldehogeschool - Campus Kantienberg', 'college', 51.0408554, 3.72861469999998);

insert into campus
values (default, 'Arteveldehogeschool - Campus Kattenberg', 'college', 51.0416838, 3.7242364);

insert into campus
values (default, 'Arteveldehogeschool - Campus Leeuwstraat', 'college', 51.0417657, 3.73163090000003);

insert into campus
values (default, 'Arteveldehogeschool - Campus Mariakerke', 'college', 51.0873544, 3.66869109999993);

insert into campus
values (default, 'Arteveldehogeschool - Campus Sint-Amandsberg', 'college', 51.0614723, 3.74731529999997);

insert into campus
values (default, 'Arteveldehogeschool - Campus Sint-Annaplein', 'college', 51.049798, 3.73519599999997);

insert into campus
values (default, 'Arteveldehogeschool - Campus Stropkaai', 'college', 51.0370077, 3.7304967);

insert into campus
values (default, 'Arteveldehogeschool - Campus Tinelstraat', 'college', 51.0733187, 3.76942310000004);

insert into campus
values (default, 'Arteveldehogeschool - Campus Watersportbaan', 'college', 51.0475753, 3.70264220000001);

insert into campus
values (default, 'Autonomous University in the German-speaking Community', 'university', 50.6177401, 6.04806110000004);

insert into campus
values (default, 'Ave Maria (École dInfirmières)', 'college', 50.46398, 3.980823);

insert into campus
values (default, 'Boston University Brussels', 'college', 50.817062, 4.4011345);

insert into campus
values (default, 'Brugge Business School', 'college', 51.1867931, 3.20310559999996);

insert into campus
values (default, 'Brussels Business Institute for Higher Education (BBI)', 'college', 50.856564, 4.4344506);

insert into campus
values (default, 'Business & Learning Center', 'college', 50.4664085, 4.86238359999993);

insert into campus
values (default, 'CERIS', 'college', 50.81459, 4.38038);

insert into campus
values (default, 'CHU UCL Namur - Site Godinne', 'university', 50.3580425, 4.88252699999998);

insert into campus
values (default, 'CHU UCLouvain - Namur Site De Dinant', 'university', 50.2628963, 4.92403549999995);

insert into campus
values (default, 'CHU UCLouvain - Namur', 'university', 50.265142, 4.94407200000001);

insert into campus
values (default, 'CVO LIMLO Diepenbeek', 'college', 50.9131561, 5.42299009999999);

insert into campus
values (default, 'CVO Sociale School', 'college', 50.8761167, 4.66175199999998);

insert into campus
values (default, 'Campus Provincial', 'college', 50.4653752, 4.83818429999997);

insert into campus
values (default, 'Centre International dEtudes de la Formation Religieuse Lumen Vitae Asbl', 'college', 50.4655556, 4.85861109999996);

insert into campus
values (default, 'Centre dÉtudes Supérieures dOptometrie Appliquee (CESOA)', 'college', 50.45973, 4.87768);

insert into campus
values (default, 'Centre médical Les Baseilles - Erpent (CHU UCL Namur)', 'college', 50.4408747, 4.90449109999997);

insert into campus
values (default, 'Conservatoire musique', 'college', 50.4553184, 3.95310770000003);

insert into campus
values (default, 'ECSSAC Asbl', 'college', 50.6399723, 5.56920279999997);

insert into campus
values (default, 'EPFC', 'college', 50.82014, 4.4033136);

insert into campus
values (default, 'ERG Saint-Luc School Search Graphique', 'college', 50.822147, 4.35733);

insert into campus
values (default, 'ESA Saint-Luc', 'college', 50.82656, 4.34904);

insert into campus
values (default, 'ESRA', 'college', 50.82916, 4.36344);

insert into campus
values (default, 'Ecole dErgologie', 'college', 50.811607, 4.380612);

insert into campus
values (default, 'Ecole de Soins Infirmiers et Pédagogie Sainte-Elisabeth ASBL', 'college', 50.459441, 4.84526900000003);

insert into campus
values (default, 'Ecole de Théatre Lassaad', 'college', 50.83211, 4.34867);

insert into campus
values (default, 'Ephec Louvain-la-Neuve', 'college', 50.6658999, 4.61221929999999);

insert into campus
values (default, 'Epitech Brussels', 'college', 50.85193, 4.36456);

insert into campus
values (default, 'Epsis St-Nicolas Namur', 'college', 50.4682152, 4.88159380000002);

insert into campus
values (default, 'ESA Saint-Luc Liège', 'college', 50.6440954, 5.58615480000003);

insert into campus
values (default, 'European Communication School (ECS)', 'college', 50.80716, 4.37057);

insert into campus
values (default, 'Faculteit voor Vergelijkende Godsdienstwetenschappen', 'college', 51.16999, 4.39541);

insert into campus
values (default, 'Faculty of Bioscience Engineering, Ghent University', 'college', 51.05278, 3.70895900000005);

insert into campus
values (default, 'Faculté Universitaire de Theologie Protestante de Bruxelles (ASBL', 'college', 50.83554, 4.40448);

insert into campus
values (default, 'Funoc', 'college', 50.41974, 4.47942);

insert into campus
values (default, 'HELHa - Site Don Bosco', 'college', 50.61078, 3.3800004);

insert into campus
values (default, 'HELHa - Site ITEHO - Mouscron', 'college', 50.74281, 3.19991);

insert into campus
values (default, 'HELHa - Site Jeanne dArc - Tournai', 'college', 50.61199, 3.3841217);

insert into campus
values (default, 'HELHa - École Normale - Braine-le-Comte', 'college', 50.608078, 4.129048);

insert into campus
values (default, 'HELHa - École Normale - Gosselies', 'college', 50.46509, 4.429812);

insert into campus
values (default, 'HELHa - École Normale - Leuze', 'college', 50.600403, 3.6221633);

insert into campus
values (default, 'HELHa - École Normale - Loverval', 'college', 50.374615, 4.473994);

insert into campus
values (default, 'HELMo - Haute Ecole Libre Mosane', 'college', 50.64438, 5.56544899999994);

insert into campus
values (default, 'HELMo Campus Guillemins', 'college', 50.622418, 5.57450700000004);

insert into campus
values (default, 'HELMo Campus de lOurthe', 'college', 50.6190907, 5.58777540000006);

insert into campus
values (default, 'HELMo Cfel', 'college', 50.6406437, 5.58449819999998);

insert into campus
values (default, 'HELMo ESAS', 'college', 50.6330136, 5.58030629999996);

insert into campus
values (default, 'HELMo ESAS', 'college', 50.6329831, 5.58040430000005);

insert into campus
values (default, 'HELMo Huy', 'college', 50.519045, 5.24219549999998);

insert into campus
values (default, 'HELMo Loncin', 'college', 50.6627975, 5.50022720000004);

insert into campus
values (default, 'HELMo Mode', 'college', 50.6328361, 5.58299320000003);

insert into campus
values (default, 'HELMo Saint-Laurent', 'college', 50.6189853, 5.58714669999995);

insert into campus
values (default, 'HELMo Saint-Roch', 'college', 50.5273778, 5.82159130000002);

insert into campus
values (default, 'HELMo Sainte-Croix', 'college', 50.6479753, 5.58119920000001);

insert into campus
values (default, 'HELMo Sainte-Julienne', 'college', 50.6185962, 5.58797040000002);

insert into campus
values (default, 'HELMo Verviers', 'college', 50.5916902, 5.87111589999995);

insert into campus
values (default, 'HEPH - Condorcet (Catégorie Economique Charleroi)', 'college', 50.41826, 4.44964);

insert into campus
values (default, 'HEPH - Condorcet (Catégorie Paramédicale Charleroi)', 'college', 50.41318, 4.46161);

insert into campus
values (default, 'HEPH - Condorcet (Catégorie Technique Charleroi)', 'college', 50.41637, 4.44709);

insert into campus
values (default, 'HEPH - Condorcet (Catégories Pédagogique et Sociale Charleroi)', 'college', 50.37593, 4.43139);

insert into campus
values (default, 'HEPH - Condorcet Mons (Economique - Pédagogique - Paramédical)', 'college', 50.46447, 3.95248);

insert into campus
values (default, 'HEPL - Haute Ecole de la Province de Liège', 'college', 50.6365777, 5.56514990000005);

insert into campus
values (default, 'HOGENT - Campus Aalst', 'college', 50.9373139, 4.03332499999999);

insert into campus
values (default, 'HOGENT - Campus Bijloke', 'college', 51.0459316, 3.71682920000001);

insert into campus
values (default, 'HOGENT - Campus Dendermonde', 'college', 51.0256839, 4.09718780000003);

insert into campus
values (default, 'HOGENT - Campus Grote Sikkel', 'college', 51.054208, 3.72632899999996);

insert into campus
values (default, 'HOGENT - Campus Ledeganck', 'college', 51.0367073, 3.72492020000004);

insert into campus
values (default, 'HOGENT - Campus Lokeren (Brouwerijstraat)', 'college', 51.1105227, 3.98996269999998);

insert into campus
values (default, 'HOGENT - Campus Lokeren (Groendreef)', 'college', 51.1094453, 3.98694279999995);

insert into campus
values (default, 'HOGENT - Campus Melle', 'college', 51.0145523, 3.78659960000005);

insert into campus
values (default, 'HOGENT - Campus Mercator', 'college', 51.0424007, 3.715416);

insert into campus
values (default, 'HOGENT - Campus Schoonmeersen', 'college', 51.0337138, 3.70144149999999);

insert into campus
values (default, 'HOGENT - Campus Vesalius', 'college', 51.0199144, 3.72722320000003);

insert into campus
values (default, 'HOGENT - FTI Lab', 'college', 51.0291214, 3.68510209999999);

insert into campus
values (default, 'HOGENT - Site Geraard de Duivelstraat', 'college', 51.0525569, 3.7281802);

insert into campus
values (default, 'HOGENT - Sporthal', 'college', 51.0343259, 3.70386050000002);

insert into campus
values (default, 'HOGENT/UGENT - Proefhoeve Bottelare', 'college', 50.9618006, 3.76016370000002);

insert into campus
values (default, 'Haute Ecole Charlemagne', 'college', 50.623473, 5.57459100000005);

insert into campus
values (default, 'Haute School Charlemagne', 'college', 50.5905687, 5.87262559999999);

insert into campus
values (default, 'Haute Ecole Fransisco Ferrer - Site Anneessens', 'college', 50.84427, 4.34335);

insert into campus
values (default, 'Haute Ecole Fransisco Ferrer - Site Palais du Midi', 'college', 50.84058, 4.34253);

insert into campus
values (default, 'Haute Ecole Galilée (IHECS)', 'college', 50.84411, 4.3494);

insert into campus
values (default, 'Haute Ecole Louvain en Hainaut (HELHa) - Charleroi', 'college', 50.42076, 4.45946);

insert into campus
values (default, 'Haute Ecole Provinciale Mons - Borinage - Centre', 'college', 50.44357, 3.81924);

insert into campus
values (default, 'Haute Ecole Robert Schuman', 'college', 49.9274212, 5.37862080000002);

insert into campus
values (default, 'Haute Ecole de Namur-liege-luxembourg', 'college', 50.4733068, 4.85510590000001);

insert into campus
values (default, 'Haute Ecole de la Province de Liège - Catégorie Technique (ISIL)', 'college', 50.6200601, 5.581547);

insert into campus
values (default, 'Haute École de la Province de Liège', 'college', 50.6204429, 5.51670319999994);

insert into campus
values (default, 'Haute École de la Ville de Liège', 'college', 50.639766, 5.56997200000001);

insert into campus
values (default, 'Haute École Albert Jacquard', 'college', 50.4668677, 4.86752809999996);

insert into campus
values (default, 'Haute École Albert Jacquard', 'college', 50.438206, 4.608021);

insert into campus
values (default, 'Haute École Bruxellles-Brabant', 'college', 50.804283, 4.372304);

insert into campus
values (default, 'Haute École Charleroi Europe', 'college', 50.45669, 3.9499347);

insert into campus
values (default, 'Haute École Francisco Ferrer - Site Bruggmann', 'college', 50.88761, 4.33119);

insert into campus
values (default, 'Haute École Francisco Ferrer - Site Lemonnier', 'college', 50.84278, 4.34488);

insert into campus
values (default, 'Haute École Francisco Ferrer - Site Terre-Neuve', 'college', 50.84034, 4.34545);

insert into campus
values (default, 'Haute École ICHEC-ECAM-ISFSC - ECAM', 'college', 50.85024, 4.45433);

insert into campus
values (default, 'Haute École ICHEC-ECAM-ISFSC - ICHEC', 'college', 50.83825, 4.407882);

insert into campus
values (default, 'Haute École ICHEC-ECAM-ISFSC - ISFSC', 'college', 50.859234, 4.3676605);

insert into campus
values (default, 'Haute École Louvain en Hainaut (HELHa Gilly)', 'college', 50.419556, 4.481119);

insert into campus
values (default, 'Haute École Louvain en Hainaut (HELHa Montignies-sur-Samre)', 'college', 50.40968, 4.4799056);

insert into campus
values (default, 'Haute École Louvain en Hainaut (HELHa Social)', 'college', 50.61106, 3.38391);

insert into campus
values (default, 'Haute École Louvain en Hainaut (HELHa) - Mouscron', 'college', 50.742404, 3.20010639999998);

insert into campus
values (default, 'Haute École Louvain en Hainaut - Fleurus', 'college', 50.4867102, 4.55178609999996);

insert into campus
values (default, 'Haute École Louvain en Hainaut Louvain-la-Neuve', 'college', 50.6700006, 4.60933090000003);

insert into campus
values (default, 'Haute École Louvain en Hainaut', 'college', 50.485268, 4.5512896);

insert into campus
values (default, 'Haute École Provinciale de Hainaut Condorcet', 'college', 50.46397, 3.95289);

insert into campus
values (default, 'Haute École Robert Schuman - Ingénieurs industriels - Département technique', 'college', 49.6721392, 5.81492379999997);

insert into campus
values (default, 'Haute École Vinci - Marie Haps, site Arlon', 'college', 50.82235, 4.3773);

insert into campus
values (default, 'Haute École Vinci - Marie Haps, site des Tilleuls', 'college', 50.835728, 4.37562);

insert into campus
values (default, 'Haute École de la Communaute Francaise Paul-Henri Spaak', 'college', 50.81461, 4.41963);

insert into campus
values (default, 'Haute École en Hainaut', 'college', 50.45989, 3.95654);

insert into campus
values (default, 'Henallux - Department Paramedic', 'college', 50.4564828, 4.83706359999996);

insert into campus
values (default, 'Henallux - Département social', 'college', 50.4643093, 4.85858610000002);

insert into campus
values (default, 'Henallux Campus Callemeyn', 'college', 49.6892008, 5.8229695);

insert into campus
values (default, 'Henallux Malonne', 'college', 50.4373868, 4.7958423);

insert into campus
values (default, 'High School of the Province of Namur', 'college', 50.464441, 4.83574899999996);

insert into campus
values (default, 'Hoger Instituut voor Godsdienstwetenschappen', 'college', 51.17622, 4.4125986);

insert into campus
values (default, 'Hoger Instituut voor Verpleegkunde Sint-Elisabeth (HIVSET)', 'college', 51.3195741, 4.94957939999995);

insert into campus
values (default, 'Hogere Zeevaartschool', 'college', 51.241272, 4.3985796);

insert into campus
values (default, 'Hogeschool PXL - Campus Diepenbeek', 'college', 50.927775, 5.384387);

insert into campus
values (default, 'Hogeschool PXL - Campus Elfde Linie', 'college', 50.937461, 5.348256);

insert into campus
values (default, 'Hogeschool PXL - Campus Guffenslaan', 'college', 50.927895, 5.342467);

insert into campus
values (default, 'Hogeschool PXL - Campus Quartier Canal', 'college', 50.9403133, 5.35288170000001);

insert into campus
values (default, 'Hogeschool PXL - Campus Vildersstraat', 'college', 50.935336, 5.344265);

insert into campus
values (default, 'Howest - Campus Brugge Centrum', 'college', 51.2150239, 3.22050569999999);

insert into campus
values (default, 'Howest - Campus Brugge Station - BST5', 'college', 51.1923035, 3.21377010000003);

insert into campus
values (default, 'Howest - Campus Buda', 'college', 50.8315457, 3.26304129999994);

insert into campus
values (default, 'Howest - Campus Fortstraat Oudenaarde', 'college', 50.8479368, 3.61301679999997);

insert into campus
values (default, 'Howest - Campus Kortrijk Penta', 'college', 50.8241846, 3.25132880000001);

insert into campus
values (default, 'Howest - Campus Kortrijk The Square', 'college', 50.824698, 3.30499599999996);

insert into campus
values (default, 'Howest - Campus Kortrijk Weide - Gebouw B', 'college', 50.824629, 3.24953900000003);

insert into campus
values (default, 'Howest - Campus Kortrijk Weide - The Level', 'college', 50.8273527, 3.25449179999998);

insert into campus
values (default, 'IESCA', 'college', 50.409977, 4.482812);

insert into campus
values (default, 'IRAM', 'college', 50.451523, 3.9827216);

insert into campus
values (default, 'Iespp Mons Nursing', 'college', 50.45727, 3.9603);

insert into campus
values (default, 'Indbe ', 'college', 50.60873, 4.12929);

insert into campus
values (default, 'Institut Enseignement Promotion Sociale', 'college', 49.5665105, 5.52946120000001);

insert into campus
values (default, 'Institut J-P Lallemand', 'college', 50.85147, 4.36067);

insert into campus
values (default, 'Institut Meurice', 'college', 50.81532, 4.29127);

insert into campus
values (default, 'Institut National Supérieur des Arts du Spectacle et des techniques de diffusion (INSAS)', 'college', 50.83487, 4.36627);

insert into campus
values (default, 'Institut Reine Astrid de Mons Iram Ensignement de Promostion Sociale', 'college', 50.45144, 3.98266);

insert into campus
values (default, 'Institut Roger Guilbert', 'college', 50.816124, 4.2953467);

insert into campus
values (default, 'Institut Sacré Coeur', 'college', 50.4564, 3.95993);

insert into campus
values (default, 'Institut Saint-Luc', 'college', 50.454845, 3.9617355);

insert into campus
values (default, 'Institut Supeérieur des Aumoniers du Travial (ISAT)', 'college', 50.87388, 4.37564);

insert into campus
values (default, 'Institut Supérieur Industriel de Bruxelles (ISIB)', 'college', 50.850376, 4.364065);

insert into campus
values (default, 'Institut Supérieur dUrbanisme et de Renovation Urbaine (ISURU)', 'college', 50.82621, 4.35196);

insert into campus
values (default, 'Institut Superieur dArchitecture Saint-Luc de Wallonie ASBL', 'college', 50.6403663, 5.57545559999994);

insert into campus
values (default, 'Institut Supérieur dArchitecture Saint-Luc de Wallonie', 'college', 50.6439035, 5.58644930000003);

insert into campus
values (default, 'Institut dEnseignement de Promotion Sociale', 'college', 49.9993572, 5.71081809999998);

insert into campus
values (default, 'Institut doptique Raymond Tibaut', 'college', 50.835278, 4.3578634);

insert into campus
values (default, 'Institut des arts de diffusion', 'college', 50.6756587, 4.61248219999993);

insert into campus
values (default, 'Institut supérieur de musique et de pédagogie de Namur', 'college', 50.4647734, 4.84647010000003);

insert into campus
values (default, 'Institute Arts And Crafts De Pierrard', 'college', 49.5734718, 5.55114270000001);

insert into campus
values (default, 'Institute D Enseignement De Promotion Sociale De La Communauté Française', 'college', 49.6728463, 5.81339479999997);

insert into campus
values (default, 'Institute Languages Vivantes De LUClouvain - Auditoires Ésope', 'college', 50.6687935, 4.61491890000002);

insert into campus
values (default, 'Institute Teaching Promotion Sociale', 'college', 50.4658079, 4.87756439999998);

insert into campus
values (default, 'Institute Teaching Social Promotion De La Comm.francaise', 'college', 49.9218196, 5.38388359999999);

insert into campus
values (default, 'Institute Technical Hospital Jeanne Darc', 'college', 50.7435075, 3.20004940000001);

insert into campus
values (default, 'Institute Technical Hospital Jeanne dArc', 'college', 50.7435, 3.20004);

insert into campus
values (default, 'Institute Technique Etienne Lenoir', 'college', 49.6728247, 5.81312079999998);

insert into campus
values (default, 'Instituut voor Tropische Geneeskunde - Onderwijs', 'college', 51.21248, 4.3992267);

insert into campus
values (default, 'International Opera Academy', 'college', 51.0432864, 3.7182699);

insert into campus
values (default, 'Ipsma Promsoc', 'college', 50.417294, 4.448844);

insert into campus
values (default, 'Isek', 'college', 50.886276, 4.33312);

insert into campus
values (default, 'KASK & Conservatorium', 'college', 51.0452121, 3.71831020000002);

insert into campus
values (default, 'Koninklijk Conservatorium Luik', 'college', 50.6347661, 5.57090629999993);

insert into campus
values (default, 'KU Leuven - AV Auditoria Complex', 'university', 50.8730577, 4.70392179999999);

insert into campus
values (default, 'KU Leuven - Auditorium Max Weber', 'university', 50.8730146, 4.70318229999998);

insert into campus
values (default, 'KU Leuven - Auditorium Oude Molen', 'university', 50.8622578, 4.68174499999998);

insert into campus
values (default, 'KU Leuven - Campus Arenberg II', 'university', 50.8605481, 4.680566);

insert into campus
values (default, 'KU Leuven - Campus Arenberg III', 'university', 50.8634435, 4.67722879999997);

insert into campus
values (default, 'KU Leuven - Campus Brussel', 'university', 50.84893, 4.3563);

insert into campus
values (default, 'KU Leuven - Campus Carolus', 'university', 51.220352, 4.403987);

insert into campus
values (default, 'KU Leuven - Campus De Nayer', 'university', 51.06792, 4.49992);

insert into campus
values (default, 'KU Leuven - Campus Geel', 'university', 51.15998, 4.961);

insert into campus
values (default, 'KU Leuven - Campus Group T', 'university', 50.8748769, 4.70777529999998);

insert into campus
values (default, 'KU Leuven - Campus Kulak Kortrijk', 'university', 50.8060793, 3.29244560000006);

insert into campus
values (default, 'KU Leuven - Campus Sint-Andries', 'university', 51.216125, 4.3979063);

insert into campus
values (default, 'KU Leuven - Campus Sint-Lucas Gent', 'university', 51.051855, 3.7173);

insert into campus
values (default, 'KU Leuven - Campus Sint-Lucas', 'university', 50.86213, 4.36757);

insert into campus
values (default, 'KU Leuven - College De Valk', 'university', 50.8779028, 4.70475829999998);

insert into campus
values (default, 'KU Leuven - Decanaat Faculteit Wetenschappen KU Leuven', 'university', 50.8630546, 4.68625610000004);

insert into campus
values (default, 'KU Leuven - Departement Burgerlijke Bouwkunde', 'university', 50.8613322, 4.68418859999997);

insert into campus
values (default, 'KU Leuven - Departement Chemie', 'university', 50.8634215, 4.67490789999999);

insert into campus
values (default, 'KU Leuven - Departement Elektrotechniek-ESAT', 'university', 50.8620895, 4.68589229999998);

insert into campus
values (default, 'KU Leuven - Departement Materiaalkunde (MTM)', 'university', 50.860639, 4.68401100000005);

insert into campus
values (default, 'KU Leuven - Departement Natuurkunde en Sterrenkunde', 'university', 50.8627344, 4.67691519999994);

insert into campus
values (default, 'KU Leuven - Departement Wiskunde', 'university', 50.8637288, 4.67808070000001);

insert into campus
values (default, 'KU Leuven - Departement computerwetenschappen', 'university', 50.8641528, 4.67875960000003);

insert into campus
values (default, 'KU Leuven - FABER', 'university', 50.8688758, 4.69399650000003);

insert into campus
values (default, 'KU Leuven - FabLab', 'university', 50.8613476, 4.68140790000007);

insert into campus
values (default, 'KU Leuven - Faculteit Bio-ingenieurswetenschappen', 'university', 50.8636382, 4.68747140000005);

insert into campus
values (default, 'KU Leuven - Faculteit Economie en Bedrijfswetenschappen', 'university', 50.8749431, 4.70045170000003);

insert into campus
values (default, 'KU Leuven - Faculteit Geneeskunde', 'university', 50.8803796, 4.67274320000001);

insert into campus
values (default, 'KU Leuven - Faculteit Ingenieurswetenschappen / Faculty of Engineering Science KU Leuven', 'university', 50.8632014, 4.68286339999997);

insert into campus
values (default, 'KU Leuven - Faculteit Letteren', 'university', 50.877337, 4.70954470000004);

insert into campus
values (default, 'KU Leuven - Faculteit Rechtsgeleerdheid', 'university', 50.8778644, 4.70469179999998);

insert into campus
values (default, 'KU Leuven - Faculteit Sociale Wetenschappen', 'university', 50.8738238, 4.70348860000001);

insert into campus
values (default, 'KU Leuven - Faculteit Theologie en Religiewetenschappen', 'university', 50.8765934, 4.70121010000003);

insert into campus
values (default, 'KU Leuven - Faculty of Engineering Technology', 'university', 50.8570217, 4.67632549999996);

insert into campus
values (default, 'KU Leuven - Gebouw De Nayer', 'university', 50.8673396, 4.69052469999997);

insert into campus
values (default, 'KU Leuven - Geo-instituut', 'university', 50.8639226, 4.67561599999999);

insert into campus
values (default, 'KU Leuven - Hoger Instituut voor Wijsbegeerte', 'university', 50.876077, 4.70674669999994);

insert into campus
values (default, 'KU Leuven - Instituut voor Plantkunde en Microbiologie', 'university', 50.8645442, 4.68893490000005);

insert into campus
values (default, 'KU Leuven - Leercentrum AGORA', 'university', 50.873697, 4.70400399999994);

insert into campus
values (default, 'KU Leuven - NanoCentre', 'university', 50.8636568, 4.67376790000003);

insert into campus
values (default, 'KU Leuven - Sports Center', 'university', 50.8661269, 4.68677230000003);

insert into campus
values (default, 'KU Leuven - Technologiecampus Aalst', 'university', 50.9321564, 4.02172029999997);

insert into campus
values (default, 'KU Leuven - Technologiecampus Gent', 'university', 51.0610519, 3.70856119999996);

insert into campus
values (default, 'KU Leuven - Thermotechnisch Instituut', 'university', 50.861088, 4.68353960000002);

insert into campus
values (default, 'KU Leuven - Topsporthal', 'university', 50.8691756, 4.69167259999995);

insert into campus
values (default, 'KU Leuven - Universiteitshal', 'university', 50.8778789, 4.70052150000004);

insert into campus
values (default, 'KU Leuven - Zwembad', 'university', 50.8698835, 4.69202250000001);

insert into campus
values (default, 'Katholieke Hogeschool Limburg VZW', 'college', 50.928472, 5.388768);

insert into campus
values (default, 'KdG Hogeschool - Campus Groenplaats', 'college', 51.218147, 4.400801);

insert into campus
values (default, 'KdG Hogeschool - Campus Hoboken', 'college', 51.17329, 4.37146);

insert into campus
values (default, 'KdG Hogeschool - Campus Linkeroever', 'college', 51.22221, 4.3763475);

insert into campus
values (default, 'KdG Hogeschool - Campus Sint-Lucas', 'college', 51.207264, 4.412787);

insert into campus
values (default, 'KdG Hogeschool - Campus Zuid', 'college', 51.20288, 4.39133);

insert into campus
values (default, 'Koninklijke Academie Voor Schone Kunsten', 'college', 51.030775, 4.10356999999999);

insert into campus
values (default, 'Koninklijke Beiaardschool Jef Denyn', 'college', 51.026268, 4.4811544);

insert into campus
values (default, 'Koninlijke Militaire School', 'college', 50.84527, 4.39231);

insert into campus
values (default, 'LUCA School Of Arts - Campus Lemmens', 'college', 50.881786, 4.68116299999997);

insert into campus
values (default, 'LUCA School of Arts - Campus Sint-Lucas Gent', 'college', 51.051855, 3.71747700000003);

insert into campus
values (default, 'LUCA School of Arts - campus C-mine', 'college', 50.982016, 5.489225);

insert into campus
values (default, 'LUCA School of Arts', 'college', 50.86133, 4.36673);

insert into campus
values (default, 'LUCA school of Arts - Campus Narafi', 'college', 50.81396, 4.330903);

insert into campus
values (default, 'LUCA school of Arts - Campus Sint-Lukas', 'college', 50.86131, 4.36675);

insert into campus
values (default, 'Ludus Academie', 'college', 50.85709, 4.34813);

insert into campus
values (default, 'Melius, Ecole Supérieure de Gestion et Communicatio', 'college', 50.842163, 4.399279);

insert into campus
values (default, 'Odisee - Campus Aalst', 'college', 50.9320925, 4.02159630000006);

insert into campus
values (default, 'Odisee - Campus Brussel Terranova', 'college', 50.85322, 4.35858);

insert into campus
values (default, 'Odisee - Campus Brussel', 'college', 50.84891, 4.3563);

insert into campus
values (default, 'Odisee - Campus Dilbeek', 'college', 50.8664403, 4.24521149999998);

insert into campus
values (default, 'Odisee - Campus Rabot', 'college', 51.0603351, 3.71000290000006);

insert into campus
values (default, 'Odisee - Campus Sint-Niklaas', 'college', 51.161349, 4.15125860000001);

insert into campus
values (default, 'Odisee - Technologiecampus Gent', 'college', 51.0602525, 3.71001820000004);

insert into campus
values (default, 'Open Universiteit', 'university', 51.222477, 4.4075212);

insert into campus
values (default, 'Pesc Fleurus', 'college', 50.4866325, 4.5512301);

insert into campus
values (default, 'Provinciaal Centrum Volwassenenonderwijs Het Perspectief, Enseignement', 'college', 51.0439889, 3.71395069999994);

insert into campus
values (default, 'School Aesthetic Biological And De Pédicurie', 'college', 50.4729031, 4.85411829999998);

insert into campus
values (default, 'School Higher Arts - Academy Des Beaux-Arts', 'college', 50.60769, 3.390006);

insert into campus
values (default, 'School voor Psychiatrische Verpleegkunde "Guislain"', 'college', 51.0662069, 3.70321739999997);

insert into campus
values (default, 'Stuvo VIVES', 'college', 51.1872171, 3.20509630000004);

insert into campus
values (default, 'Technische Universiteit Louvain (EPL) UCLouvain', 'university', 50.6683004, 4.6208239);

insert into campus
values (default, 'The International Academy of Osteopathy (IAO)', 'college', 51.0577034, 3.73924349999993);

insert into campus
values (default, 'Thomas More - Campus De Ham', 'college', 51.02256, 4.48791);

insert into campus
values (default, 'Thomas More - Campus De Nayer', 'college', 51.06845, 4.49962);

insert into campus
values (default, 'Thomas More - Campus De Vest', 'college', 51.02373, 4.48814);

insert into campus
values (default, 'Thomas More - Campus Geel', 'college', 51.16098, 4.96151);

insert into campus
values (default, 'Thomas More - Campus Kruidtuin', 'college', 51.02462, 4.4851);

insert into campus
values (default, 'Thomas More - Campus Lier', 'college', 51.13412, 4.5664754);

insert into campus
values (default, 'Thomas More - Campus Lucas Faydherbe', 'college', 51.02499, 4.4877);

insert into campus
values (default, 'Thomas More - Campus National', 'college', 51.21173, 4.39811);

insert into campus
values (default, 'Thomas More - Campus Sanderus', 'college', 51.20739, 4.4051);

insert into campus
values (default, 'Thomas More - Campus Sint-Andries', 'college', 51.21608, 4.39726);

insert into campus
values (default, 'Thomas More - Campus Turnhout', 'college', 51.3173, 4.92893);

insert into campus
values (default, 'Thomas More - Campus Vorselaar', 'college', 51.20101, 4.77269);

insert into campus
values (default, 'Thomas More - Lesplaats Duffel (SNOR)', 'college', 51.0953, 4.49607);

insert into campus
values (default, 'Thomas More - Lesplaats Herentals', 'college', 51.17517, 4.83497);

insert into campus
values (default, 'Thomas More - Lesplaats Lier (SAL)', 'college', 51.1328, 4.56677);

insert into campus
values (default, 'Thomas More - Lesplaats Sint-Niklaas', 'college', 51.16287, 4.13633);

insert into campus
values (default, 'Thomas More - Lesplaats Turnhout (High Tech)', 'college', 51.31456, 4.92106);

insert into campus
values (default, 'Thomas More - Lesplaats Turnhout (Hivset)', 'college', 51.31946, 4.94894);

insert into campus
values (default, 'Thomas More - Lesplaats Westerlo', 'college', 51.08847, 4.91253);

insert into campus
values (default, 'UAntwerpen - Campus Ambtmanstraat Productontwikkeling', 'university', 51.22267, 4.40652);

insert into campus
values (default, 'UAntwerpen - Campus Drie Eiken', 'university', 51.16216, 4.4035);

insert into campus
values (default, 'UAntwerpen - Campus Groenenborger', 'university', 51.17818, 4.41577);

insert into campus
values (default, 'UAntwerpen - Campus Middelheim', 'university', 51.18482, 4.41985);

insert into campus
values (default, 'UAntwerpen - Campus Mutsaard', 'university', 51.22316, 4.40673);

insert into campus
values (default, 'UAntwerpen - Campus Paardenmarkt', 'university', 51.22502, 4.4114714);

insert into campus
values (default, 'UAntwerpen - Stadscampus', 'university', 51.22089, 4.4109);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Clenardus', 'college', 50.9898645, 5.05087800000001);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Comenius', 'college', 50.8790303, 4.7152691);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Diepenbeek', 'college', 50.928991, 5.395086);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Gasthuisberg', 'college', 50.8806714, 4.67444509999996);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Hemelrijk', 'college', 50.9304718, 5.34018860000003);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Hertogstraat', 'college', 50.8561346, 4.70303630000001);

insert into campus
values (default, 'UC Leuven-Limburg - Campus LiZa', 'college', 50.957529, 5.520066);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Oude Luikerbaan', 'college', 50.9210849, 5.34590449999996);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Quadri', 'college', 50.93107, 5.397723);

insert into campus
values (default, 'UC Leuven-Limburg - Campus Sociale School', 'college', 50.8763158, 4.66179620000003);

insert into campus
values (default, 'UCLouvain - Brussel Sint-Gillis (LOCI)', 'university', 50.8212318, 4.34955300000001);

insert into campus
values (default, 'UCLouvain - Brussel Woluwe', 'university', 50.8504229, 4.45724849999999);

insert into campus
values (default, 'UCLouvain - Brussels Woluwe', 'university', 50.8501523, 4.45369949999997);

insert into campus
values (default, 'UCLouvain - Charleroi', 'university', 50.4094173, 4.48170189999996);

insert into campus
values (default, 'UCLouvain - Computer Science (ICTEAM INGI)', 'university', 50.6685724, 4.62159099999997);

insert into campus
values (default, 'UCLouvain - FIAL', 'university', 50.6695501, 4.6102952);

insert into campus
values (default, 'UCLouvain - FUCaM Bergen', 'university', 50.4529289, 3.98450869999999);

insert into campus
values (default, 'UCLouvain - Faculteit Economische, Sociale, Politieke en Communicatiewetenschappen (ESPO)', 'university', 50.6678157, 4.6117084);

insert into campus
values (default, 'UCLouvain - Faculteit Rechten en Criminologie', 'university', 50.6679955, 4.61082499999998);

insert into campus
values (default, 'UCLouvain - Faculteit Wetenschappen', 'university', 50.6685409, 4.61951390000002);

insert into campus
values (default, 'UCLouvain - Site de Tournai de la Faculté darchitecture, dingénierie architecturale, durbanisme', 'university', 50.6061929, 3.39759240000001);

insert into campus
values (default, 'UCLouvain - Social Media Lab', 'university', 50.45287, 3.98085279999998);

insert into campus
values (default, 'UCLouvain CLL - Taleninstituut', 'university', 50.6711016, 4.61017370000002);

insert into campus
values (default, 'UCLouvain Saint-Louis - Site Botanique', 'university', 50.85404, 4.362193);

insert into campus
values (default, 'UCLouvain Saint-Louis - Site Marie Haps', 'university', 50.83869, 4.37202);

insert into campus
values (default, 'ULB - Campus Erasme', 'university', 50.8142, 4.26345);

insert into campus
values (default, 'ULB - Campus Flagey', 'university', 50.8272591, 4.3735302);

insert into campus
values (default, 'ULB - Campus Plaine', 'university', 50.8172, 4.40225);

insert into campus
values (default, 'ULB - Campus Solbosch', 'university', 50.81549, 4.38301);

insert into campus
values (default, 'ULB - Campus Uccle', 'university', 50.81391, 4.36639);

insert into campus
values (default, 'ULB - Campus Usquare', 'university', 50.81144, 4.38193);

insert into campus
values (default, 'UMons - Campus Charleroi', 'university', 50.41481, 4.45094);

insert into campus
values (default, 'UMons - Campus Polytechnique', 'university', 50.45168, 3.95913);

insert into campus
values (default, 'UMons - Campus Science', 'university', 50.45858, 3.95143);

insert into campus
values (default, 'Universiteit Gent - Campus Aula', 'university', 51.0513093, 3.72399289999998);

insert into campus
values (default, 'Universiteit Gent - Campus Boekentoren', 'university', 51.0442905, 3.72502229999998);

insert into campus
values (default, 'Universiteit Gent - Campus Coupure', 'university', 51.0528015, 3.70889999999997);

insert into campus
values (default, 'Universiteit Gent - Campus Dunant', 'university', 51.0488606, 3.70399599999996);

insert into campus
values (default, 'Universiteit Gent - Campus Gontrode', 'university', 50.9750014, 3.80584780000004);

insert into campus
values (default, 'Universiteit Gent - Campus HILO', 'university', 51.0480162, 3.70368710000002);

insert into campus
values (default, 'Universiteit Gent - Campus Heide (Dierenkliniek)', 'university', 50.9990133, 3.7662325);

insert into campus
values (default, 'Universiteit Gent - Campus Heymans', 'university', 51.0254676, 3.73018560000003);

insert into campus
values (default, 'Universiteit Gent - Campus Ledeganck', 'university', 51.0364571, 3.72384409999995);

insert into campus
values (default, 'Universiteit Gent - Campus Melle', 'university', 50.9797878, 3.81944769999996);

insert into campus
values (default, 'Universiteit Gent - Campus Mercator', 'university', 51.043621, 3.71236499999998);

insert into campus
values (default, 'Universiteit Gent - Campus Merelbeke', 'university', 50.9983726, 3.76687079999999);

insert into campus
values (default, 'Universiteit Gent - Campus Proeftuin', 'university', 51.0239101, 3.74067109999999);

insert into campus
values (default, 'Universiteit Gent - Campus Rommelaere', 'university', 51.0455764, 3.71891949999997);

insert into campus
values (default, 'Universiteit Gent - Campus Schoonmeersen', 'university', 51.0311436, 3.70639900000003);

insert into campus
values (default, 'Universiteit Gent - Campus Sterre', 'university', 51.0242436, 3.71062110000003);

insert into campus
values (default, 'Universiteit Gent - Campus Tweekerken', 'university', 51.0438428, 3.72781520000001);

insert into campus
values (default, 'Universiteit Gent - Campus UZ Gent', 'university', 51.0227166, 3.72978599999999);

insert into campus
values (default, 'Universiteit Gent - Campus Ufo', 'university', 51.0472812, 3.72805319999998);

insert into campus
values (default, 'Universiteit Gent - De Krook', 'university', 51.0489303, 3.72886530000005);

insert into campus
values (default, 'Universiteit Gent - Het Pand', 'university', 51.053035, 3.71959620000007);

insert into campus
values (default, 'Universiteit Gent - Sportcomplex / zwembad GUSB', 'university', 51.0475487, 3.70264689999999);

insert into campus
values (default, 'Universiteit Gent - Tech Lane Ghent Science Park/Campus Ardoyen', 'university', 51.0100414, 3.70971050000003);

insert into campus
values (default, 'Universiteit Hasselt - Campus Diepenbeek', 'university', 50.9320495, 5.39614870000003);

insert into campus
values (default, 'Universiteit Hasselt - Campus Hasselt', 'university', 50.933532, 5.342293);

insert into campus
values (default, 'Université Européenne dEcriture (UEE)', 'university', 50.804443, 4.341777);

insert into campus
values (default, 'Université Libre Internationale - Institut des Hautes Études de Bruxelles', 'university', 50.84407, 4.34939);

insert into campus
values (default, 'Université Ouverte de la Fédération Wallonie-Bruxelles', 'college', 50.411407, 4.451213);

insert into campus
values (default, 'Université de Namur', 'university', 50.4661979, 4.86012129999995);

insert into campus
values (default, 'Université de Namur', 'university', 50.4452272, 5.02079479999998);

insert into campus
values (default, 'University of Liege - Auditorium of the Opera', 'university', 50.6432279, 5.57170889999998);

insert into campus
values (default, 'Université de Liège - B53 Aquapôle', 'university', 50.5856233, 5.5584244);

insert into campus
values (default, 'Université de Liège - Campus Arlon', 'university', 49.6803583, 5.82406879999996);

insert into campus
values (default, 'Université de Liège - Campus Gembloux', 'university', 50.5617069, 4.69650669999999);

insert into campus
values (default, 'Université de Liège - Campus Sart-Tilman', 'university', 50.5830803, 5.55906400000003);

insert into campus
values (default, 'Université de Liège - Centre Ville', 'university', 50.6370205, 5.5629338);

insert into campus
values (default, 'Université de Liège - Centre Ville', 'university', 50.6278403, 5.57186290000004);

insert into campus
values (default, 'VIVES - Campus Brugge Station', 'college', 51.1937981, 3.21809989999997);

insert into campus
values (default, 'VIVES - Campus Brugge Xaverianenstraat', 'college', 51.1874237, 3.20342289999996);

insert into campus
values (default, 'VIVES - Campus Kortrijk', 'college', 50.8058616, 3.28408869999998);

insert into campus
values (default, 'VIVES - Campus Oostende Station', 'college', 51.2259207, 2.92619360000003);

insert into campus
values (default, 'VIVES - Campus Roeselare', 'college', 50.9386463, 3.11908459999995);

insert into campus
values (default, 'VIVES - Campus Torhout', 'college', 51.0687571, 3.10668299999998);

insert into campus
values (default, 'VIVES - Campus VLOC - Vlaams Luchtvaartopleidingscentrum', 'college', 51.2003629, 2.85558049999997);

insert into campus
values (default, 'VUB - Brussels Health Campus', 'university', 50.88701, 4.30542);

insert into campus
values (default, 'VUB - Brussels Photonics Campus', 'university', 50.77195, 4.05682);

insert into campus
values (default, 'VUB - Campus Elsene', 'university', 50.82271, 4.39573);

insert into campus
values (default, 'VUB - Vesalius College', 'university', 50.82142, 4.39165);

insert into campus
values (default, 'Vasalius College', 'college', 50.82227, 4.376978);

insert into campus
values (default, 'Vatel International Business School Hotel and Tourism Management', 'college', 50.8339112, 4.3518169);

insert into campus
values (default, 'Vlerick Business School', 'college', 51.0515497, 3.73008249999998);

insert into campus
values (default, 'Vlerick Business School', 'college', 50.8743547, 4.7018051);

insert into campus
values (default, 'Vlerick Business School', 'college', 50.85635, 4.35703);

insert into campus
values (default, 'ZoWe verpleegkunde', 'college', 51.2180025, 2.91540199999997);

insert into campus
values (default, 'ZoWe verpleegkunde', 'college', 51.1942674, 3.20823559999997);

insert into campus
values (default, 'École Industrielle de Thuin-Montigny', 'college', 50.377254, 4.3785286);

insert into campus
values (default, 'École Industrielle et Commerciale de Courcelles', 'college', 50.46143, 4.3794565);

insert into campus
values (default, 'École Industrielle et Commerciale', 'college', 50.566734, 4.1659102);

insert into campus
values (default, 'École Supérieure Communale des Arts de lImage', 'college', 50.844685, 4.439759);

insert into campus
values (default, 'École Supérieure des Arts de la Ville de Liège', 'university', 50.6471986, 5.56812020000007);

insert into campus
values (default, 'École Supérieure des Sciences Fiscales', 'college', 50.838215, 4.408346);

insert into campus
values (default, 'École dInfirmièr(e)s (IESCA) - Charleroi', 'college', 50.40842, 4.48138);

insert into campus
values (default, 'École dInfirmièr(e)s (IESCA) - La Louvière', 'college', 50.4754, 4.215695);

insert into campus
values (default, 'École dInfirmièr(e)s (IESCA) - Mons', 'college', 50.436993, 3.8301528);

insert into campus
values (default, 'École supérieure des arts du cirque', 'college', 50.815536, 4.294664);

