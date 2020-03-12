from django.db import models
# from datetime import date

class Category(models.Model):
    """Model representing a transaction category."""
    name = models.CharField(max_length=200, help_text='Enter a transaction category (e.g. Food)')
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class CCY(models.Model):
    """Model representing a currency."""
    name = models.CharField(max_length=10, help_text='Enter a short name for a currency (e.g. RUB)')
    full_name = models.CharField(max_length=200, help_text='Enter a full name for a currency (e.g. Russian ruble)')

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.name, self.full_name)


class Transactions(models.Model):
    """Model representing a transaction record."""
    tr_date = models.DateField(null=False, blank=False)
    tr_time = models.TimeField(null=True, blank=True)
    Sum = models.DecimalField(max_digits=19, decimal_places=2, help_text='Enter a transaction sum')
     
    TR_DIRS = (
        ('-', 'Spending'),
        ('+', 'Obtaining'),
    )
    
    tr_direction = models.CharField(
        max_length=1,
        choices=TR_DIRS,
        blank=True,
        default='+',
        help_text="Whether you're spending (-) or receiving (+)")

    CCY = models.ForeignKey('CCY', on_delete=models.SET_NULL, null=True)
    Category = models.ManyToManyField(Category, help_text="Select a Category for this transaction")
    
    def display_sum(self):
        """Shows sum with a +/- sign"""
        return '{}{}'.format(self.tr_direction, self.Sum)
    
    def display_category(self):
        """Creates a string for the Category. This is required to display genre in Admin."""
        return ', '.join([cat.name for cat in self.Category.all()])

    display_category.short_description = 'Categories'
    
    Content = models.CharField(max_length=200, help_text='Enter a transaction category (e.g. Food)')
  
    
    class Meta:
        ordering = ['tr_date', 'tr_time', 'Sum', 'CCY']

    
    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1}) {2}{3} {4} {5}'.format(self.tr_date, self.tr_time, self.tr_direction, self.Sum, self.CCY, self.Content)


class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(upload_to='uploaded_files')