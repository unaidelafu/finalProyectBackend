class Employee:
      
      def __init__(self, id, sid, name_1, name_2, mail, phone_num, pswrd, status,jobId, job, admin,img_url):
            self.id = id
            self.sid = sid
            self.name_1 =  name_1
            self.name_2 = name_2
            self.mail =  mail
            self.phone_num = phone_num            
            self.pswrd = pswrd
            self.status = status
            self.jobId = jobId
            self.job = job
            self.admin = admin
            self.img_url = img_url

      #serialize to prepare for json

      def serialize(self):
        return {
            'id': self.id, 
            'sid': self.sid,
            'name_1': self.name_1,
            'name_2': self.name_2,
            'mail': self.mail,
            'phone_num': self.phone_num,
            'pswrd': self.pswrd,
            'status': self.status,
            'job_id': self.jobId,
            'job': self.job,
            'admin': self.admin,
            'img_url': self.img_url
        }
      