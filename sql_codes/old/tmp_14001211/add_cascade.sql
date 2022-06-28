alter TABLE phoneNumber
ADD FOREIGN key (name_id) REFERENCES names(id) ON DELETE CASCADE ON UPDATE CASCADE

alter TABLE email
ADD FOREIGN key (name_id) REFERENCES names(id) ON DELETE CASCADE

alter TABLE Address
ADD FOREIGN key (name_id) REFERENCES names(id) ON DELETE CASCADE


alter TABLE Address
ADD FOREIGN key (name_id) REFERENCES names(id) ON UPDATE CASCADE

alter TABLE email
ADD FOREIGN key (name_id) REFERENCES names(id) ON Update CASCADE

alter TABLE phoneNumber
ADD FOREIGN key (name_id) REFERENCES names(id) ON Update CASCADE
